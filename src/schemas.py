"""
Standardized JSON Message Schemas for Eco-Loop Building Telemetry and Actuator Stream.

Architected to mirror production BACnet / Modbus / IoT Gateway payload contracts.
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class ZoneTelemetry:
    zone_name: str
    temperature_c: float
    occupancy_count: int
    pmv: float

@dataclass
class SensorTelemetryPayload:
    """
    Standardized payload published by EMS / BACnet Gateway stream.
    """
    timestamp: str
    timestep: int
    hour: int
    outdoor_temp_c: float
    grid_carbon_intensity_gco2_kwh: float
    cumulative_energy_kwh: float
    zones: Dict[str, Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ActionDecisionPayload:
    """
    Standardized action payload published by LLM Agent decision engine.
    """
    timestamp: str
    zone: str
    cooling_setpoint: float
    heating_setpoint: float
    confidence_score: float
    justification: str
    flagged_anomaly: bool
    reasoning_chain: Optional[Dict[str, str]] = None
    counterfactual: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
