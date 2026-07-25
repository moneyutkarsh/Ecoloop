"""
Grid Carbon Intensity Signal & Lookahead Forecast Module.
Reads real historical grid carbon intensity data from PJM ComEd (EIA-930 / Electricity Maps dataset)
covering Chicago, IL with linear 15-minute interpolation and synthetic fallback protection.
"""
import logging
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

# Data file path
BASE_DIR = Path(__file__).resolve().parent.parent
REAL_CARBON_CSV_PATH = BASE_DIR / "data" / "real_grid_carbon_chicago_2024.csv"

# Synthetic fallback curve (PJM ComEd diurnal shape)
SYNTHETIC_HOURLY_CARBON: Dict[int, float] = {
    0: 340.0, 1: 330.0, 2: 320.0, 3: 315.0, 4: 325.0, 5: 360.0,
    6: 450.0, 7: 510.0, 8: 480.0, 9: 390.0, 10: 270.0, 11: 210.0,
    12: 180.0, 13: 190.0, 14: 210.0, 15: 240.0, 16: 310.0, 17: 480.0,
    18: 580.0, 19: 620.0, 20: 590.0, 21: 520.0, 22: 430.0, 23: 370.0
}

def load_real_carbon_data() -> Dict[int, float]:
    """
    Loads real historical grid carbon intensity data from data/real_grid_carbon_chicago_2024.csv.
    Falls back to synthetic curve if file is missing or malformed.
    """
    if not REAL_CARBON_CSV_PATH.exists():
        logger.warning(
            "[CARBON FALLBACK ACTIVE] '%s' not found. Falling back to synthetic grid carbon curve.",
            REAL_CARBON_CSV_PATH
        )
        return SYNTHETIC_HOURLY_CARBON

    try:
        df = pd.read_csv(REAL_CARBON_CSV_PATH)
        if 'hour' in df.columns and 'carbon_intensity_gco2_kwh' in df.columns:
            hourly_map = dict(zip(df['hour'].astype(int), df['carbon_intensity_gco2_kwh'].astype(float)))
            logger.info("Loaded real PJM ComEd grid carbon dataset from %s", REAL_CARBON_CSV_PATH.name)
            return hourly_map
        else:
            logger.warning("[CARBON FALLBACK ACTIVE] Invalid schema in %s. Using synthetic curve.", REAL_CARBON_CSV_PATH.name)
            return SYNTHETIC_HOURLY_CARBON
    except Exception as e:
        logger.warning("[CARBON FALLBACK ACTIVE] Error reading %s (%s). Using synthetic curve.", REAL_CARBON_CSV_PATH.name, e)
        return SYNTHETIC_HOURLY_CARBON

# Global cached hourly lookup table
HOURLY_CARBON_MAP: Dict[int, float] = load_real_carbon_data()

def get_carbon_intensity(hour_of_day: int, minute: int = 0) -> float:
    """
    Returns grid carbon intensity (gCO2/kWh) for specified hour and minute,
    performing 15-minute linear interpolation between hourly data points.
    """
    h = int(hour_of_day) % 24
    next_h = (h + 1) % 24
    frac = max(0.0, min(1.0, float(minute) / 60.0))

    val_current = HOURLY_CARBON_MAP.get(h, 350.0)
    val_next = HOURLY_CARBON_MAP.get(next_h, 350.0)

    interpolated_val = (1.0 - frac) * val_current + frac * val_next
    return round(interpolated_val, 2)

def is_low_carbon_hour(hour_of_day: int, minute: int = 0) -> bool:
    return get_carbon_intensity(hour_of_day, minute) < 250.0

def is_high_carbon_hour(hour_of_day: int, minute: int = 0) -> bool:
    return get_carbon_intensity(hour_of_day, minute) > 500.0

def get_lookahead_forecast(hour_of_day: int, hours_ahead: int = 2) -> Dict[str, Any]:
    """
    Returns 2-hour forward-looking forecast of real grid carbon intensity, outdoor temperature,
    and zone occupancy schedule to enable predictive pre-conditioning.
    """
    current_h = int(hour_of_day) % 24
    forecast_hours = [(current_h + i) % 24 for i in range(1, hours_ahead + 1)]

    # 1. Real Carbon Forecast
    carbon_forecast = [get_carbon_intensity(h) for h in forecast_hours]

    # 2. Outdoor Weather Forecast (Chicago summer day curve)
    hourly_temps = [21.5, 20.8, 20.2, 19.8, 19.5, 20.5, 22.0, 24.0, 26.2, 28.5, 30.2, 31.8, 32.5, 33.0, 32.8, 32.0, 30.5, 28.8, 26.8, 25.2, 24.0, 23.0, 22.2, 21.6]
    weather_forecast = [hourly_temps[h] for h in forecast_hours]

    # 3. Multi-Zone Occupancy Schedule Forecast
    occ_forecast = {}
    for z_name in ["Open_Office", "Executive_Suite", "Conference_Room"]:
        occ_list = []
        for h in forecast_hours:
            if z_name == "Open_Office":
                occ = 10 if (8 <= h < 18) else 0
            elif z_name == "Executive_Suite":
                occ = 2 if (9 <= h < 17) else 0
            else:
                occ = 12 if (10 <= h < 12) else (8 if (14 <= h < 16) else 0)
            occ_list.append(occ)
        occ_forecast[z_name] = occ_list

    return {
        "current_hour": current_h,
        "forecast_hours": forecast_hours,
        "carbon_forecast_gco2_kwh": carbon_forecast,
        "weather_forecast_temp_c": weather_forecast,
        "occupancy_forecast": occ_forecast
    }

if __name__ == "__main__":
    fc = get_lookahead_forecast(9, hours_ahead=2)
    print("[+] 2-Hour Real Carbon Lookahead Forecast for 09:00:")
    print(fc)
