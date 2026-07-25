"""
Configuration constants and validation layer for Eco-Loop Building Agents.
"""
import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Base Paths
BASE_DIR: Path = Path(__file__).resolve().parent.parent
MODELS_DIR: Path = BASE_DIR / "models"
LOGS_DIR: Path = BASE_DIR / "logs"
DOCS_DIR: Path = BASE_DIR / "docs"

# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)
DOCS_DIR.mkdir(exist_ok=True)

# File Paths
BASELINE_IDF_PATH: Path = MODELS_DIR / "baseline_doe_reference.idf"
BASELINE_CUSTOM_IDF_PATH: Path = MODELS_DIR / "baseline_custom.idf"
WEATHER_EPW_PATH: Path = MODELS_DIR / "weather.epw"
BASELINE_CSV_PATH: Path = LOGS_DIR / "baseline_output.csv"
AI_CSV_PATH: Path = LOGS_DIR / "ai_output.csv"
DECISIONS_LOG_PATH: Path = LOGS_DIR / "decisions_log.jsonl"

# Simulation Timestep & Comfort Bounds
TIMESTEPS_PER_HOUR: int = 4  # 15-minute timesteps
TOTAL_HOURS: int = 24
TOTAL_TIMESTEPS: int = TOTAL_HOURS * TIMESTEPS_PER_HOUR  # 96 timesteps for a 24h run

# Thermal Comfort Bounds (Fanger PMV ISO 7730)
COMFORT_PMV_MIN: float = -0.5
COMFORT_PMV_MAX: float = 0.5
COMFORT_TEMP_MIN_C: float = 21.0
COMFORT_TEMP_MAX_C: float = 24.0

# HVAC Setpoint Limits
SETPOINT_COOLING_DEFAULT_C: float = 22.5
SETPOINT_HEATING_DEFAULT_C: float = 20.0
SETPOINT_COOLING_MIN_C: float = 20.0
SETPOINT_COOLING_MAX_C: float = 26.0
SETPOINT_HEATING_MIN_C: float = 18.0
SETPOINT_HEATING_MAX_C: float = 22.0

# Lighting Levels
LIGHTING_LEVEL_DEFAULT: float = 1.0  # 100%

def validate_config() -> bool:
    """
    Startup validation layer to fail fast if configuration parameters or paths are invalid.
    
    Returns:
        bool: True if configuration is valid.
        
    Raises:
        AssertionError: If any thermal, setpoint, or timestep configuration is physically invalid.
    """
    assert COMFORT_PMV_MIN < COMFORT_PMV_MAX, f"Invalid PMV bounds: {COMFORT_PMV_MIN} >= {COMFORT_PMV_MAX}"
    assert COMFORT_TEMP_MIN_C < COMFORT_TEMP_MAX_C, f"Invalid temp bounds: {COMFORT_TEMP_MIN_C} >= {COMFORT_TEMP_MAX_C}"
    assert SETPOINT_COOLING_MIN_C < SETPOINT_COOLING_MAX_C, "Invalid cooling setpoint range"
    assert SETPOINT_HEATING_MIN_C < SETPOINT_HEATING_MAX_C, "Invalid heating setpoint range"
    assert TIMESTEPS_PER_HOUR > 0, "TIMESTEPS_PER_HOUR must be positive"
    assert TOTAL_HOURS > 0, "TOTAL_HOURS must be positive"
    logger.info("Config validation layer passed successfully.")
    return True

# Run validation on import
validate_config()
