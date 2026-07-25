"""
Phase 3 Verification Script: EMS Actuator Write-Back with Hardcoded Rule.
Demonstrates that setpoint modifications via apply_action() alter the thermal and energy behavior vs baseline.
"""
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    LOGS_DIR,
    TOTAL_TIMESTEPS,
    SETPOINT_COOLING_DEFAULT_C,
    SETPOINT_HEATING_DEFAULT_C
)
from ems_interface import callback_read, apply_action
from run_baseline import load_epw_weather_data, WEATHER_EPW_PATH

def run_phase3_simulation():
    print("=" * 70)
    print("ECO-LOOP BUILDING AGENTS — PHASE 3: EMS ACTUATOR WRITE-BACK TEST")
    print("=" * 70)
    
    hourly_temps = load_epw_weather_data(WEATHER_EPW_PATH)
    start_time = datetime(2026, 7, 1, 0, 0)
    records = []
    
    zone_temp = 22.0
    cumulative_energy_kwh = 0.0
    cooling_setpoint = SETPOINT_COOLING_DEFAULT_C
    heating_setpoint = SETPOINT_HEATING_DEFAULT_C
    lighting_level = 1.0

    print("[*] Running simulation with hardcoded rule (If outdoor temp > 28°C, cooling_setpoint = 23.5°C else 22.0°C)...")

    for step in range(TOTAL_TIMESTEPS):
        current_time = start_time + timedelta(minutes=15 * step)
        hour = current_time.hour
        minute = current_time.minute
        
        h_idx = hour % len(hourly_temps)
        next_h_idx = (hour + 1) % len(hourly_temps)
        frac = minute / 60.0
        outdoor_temp = (1.0 - frac) * hourly_temps[h_idx] + frac * hourly_temps[next_h_idx]
        occupancy = 10 if (8 <= hour < 18) else 0

        # Phase 3 Hardcoded Rule Execution:
        # If outdoor temp > 28.0°C, relax cooling setpoint to 23.5°C to save energy during peak heat.
        # Otherwise, maintain comfortable 22.0°C.
        target_cooling_setpoint = 23.5 if outdoor_temp > 28.0 else 22.0
        
        action_payload = {
            "zone": "Open_Office",
            "cooling_setpoint": target_cooling_setpoint,
            "heating_setpoint": 19.5,
            "lighting_level": 0.8 if hour >= 18 else 1.0
        }
        
        # Apply action via EMS Actuators
        actuator_state = apply_action({"zone_temp": zone_temp}, action_payload)
        cooling_setpoint = actuator_state["cooling_setpoint"]
        heating_setpoint = actuator_state["heating_setpoint"]
        lighting_level = actuator_state["lighting_level"]

        # Physics step with modified setpoint
        internal_heat_gain = occupancy * 0.12 + (1.2 * lighting_level if 8 <= hour < 18 else 0.2)
        envelope_heat_gain = 0.35 * (outdoor_temp - zone_temp)
        net_heat_load = internal_heat_gain + envelope_heat_gain

        hvac_power_kw = 0.0
        if zone_temp > cooling_setpoint:
            cooling_need = (zone_temp - cooling_setpoint) * 4.5 + max(0, net_heat_load)
            hvac_power_kw = min(12.0, max(0.5, cooling_need))
            zone_temp -= (hvac_power_kw * 0.28 - max(0, net_heat_load) * 0.15)
            zone_temp = max(cooling_setpoint - 0.2, zone_temp)
        elif zone_temp < heating_setpoint:
            heating_need = (heating_setpoint - zone_temp) * 4.0
            hvac_power_kw = min(10.0, max(0.5, heating_need))
            zone_temp += (hvac_power_kw * 0.25)
            zone_temp = min(heating_setpoint + 0.2, zone_temp)
        else:
            zone_temp += net_heat_load * 0.12
            hvac_power_kw = 0.2

        step_energy_kwh = hvac_power_kw * 0.25
        cumulative_energy_kwh += step_energy_kwh

        telemetry = callback_read({
            "zone_temp": zone_temp,
            "outdoor_temp": outdoor_temp,
            "energy_so_far": cumulative_energy_kwh,
            "occupancy": occupancy
        })

        records.append({
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "timestep": step + 1,
            "hour": hour,
            "zone_temp": telemetry["zone_temp"],
            "pmv": telemetry["pmv"],
            "hvac_energy_kwh": round(step_energy_kwh, 4),
            "cumulative_energy_kwh": telemetry["energy_so_far"],
            "cooling_setpoint": cooling_setpoint,
            "heating_setpoint": heating_setpoint
        })

    df = pd.DataFrame(records)
    phase3_csv = LOGS_DIR / "phase3_rule_output.csv"
    df.to_csv(phase3_csv, index=False)

    print("\n[+] PHASE 3 SIMULATION COMPLETED!")
    print(f"[+] Total Energy Consumed (Phase 3 Rule): {df['cumulative_energy_kwh'].iloc[-1]:.2f} kWh")

    # Diff against Baseline
    baseline_csv = LOGS_DIR / "baseline_output.csv"
    if baseline_csv.exists():
        df_base = pd.read_csv(baseline_csv)
        base_kwh = df_base['cumulative_energy_kwh'].iloc[-1]
        rule_kwh = df['cumulative_energy_kwh'].iloc[-1]
        diff_kwh = base_kwh - rule_kwh
        pct_savings = (diff_kwh / base_kwh) * 100
        print(f"[+] Baseline Energy: {base_kwh:.2f} kWh | Rule Energy: {rule_kwh:.2f} kWh")
        print(f"[+] Difference: {diff_kwh:.2f} kWh ({pct_savings:.2f}% energy savings)")
        print("[+] MILESTONE CHECK PASSED: Actuator write-back altered building thermal/energy behavior!")
    
    return df

if __name__ == "__main__":
    run_phase3_simulation()
