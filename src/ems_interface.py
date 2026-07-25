"""
EMS Interface Callback Module for Eco-Loop Building Agents.

Provides sensor registration, state reading callbacks, actuator write-back functions,
multi-zone state tracking, and Fanger PMV (ISO 7730) thermal comfort calculation.
"""
import math
import logging
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger(__name__)

def calculate_pmv(
    ta: float,
    tr: Optional[float] = None,
    vel: float = 0.1,
    rh: float = 50.0,
    met: float = 1.2,
    clo: float = 0.6
) -> float:
    """
    Computes Fanger PMV (Predicted Mean Vote) thermal comfort index according to ISO 7730.

    Args:
        ta (float): Air temperature in °C.
        tr (Optional[float]): Mean radiant temperature in °C. Defaults to ta if None.
        vel (float): Relative air velocity in m/s. Defaults to 0.1.
        rh (float): Relative humidity in %. Defaults to 50.0.
        met (float): Metabolic rate in met (1 met = 58.15 W/m²). Defaults to 1.2.
        clo (float): Clothing insulation in clo (1 clo = 0.155 m²K/W). Defaults to 0.6.

    Returns:
        float: Fanger PMV index bounded between -3.0 (very cold) and +3.0 (very hot).
               Target comfort envelope per ISO 7730 is [-0.5, +0.5].
    """
    if tr is None:
        tr = ta

    m: float = met * 58.15  # metabolic rate in W/m2
    w: float = 0.0          # external work in W/m2
    mw: float = m - w
    
    icl: float = clo * 0.155  # thermal resistance of clothing in m2K/W
    fcl: float = 1.0 + 1.29 * icl if icl <= 0.078 else 1.05 + 0.645 * icl

    pa: float = rh * 10.0 * math.exp(16.6536 - 4030.183 / (ta + 235.0))
    hcf: float = 12.1 * math.sqrt(vel)
    tcl: float = ta + (35.5 - ta) / (3.5 * (6.3 + 2.29 * vel))
    
    for _ in range(20):
        tcla: float = tcl + 273.15
        tra: float = tr + 273.15

        hcr: float = 2.38 * math.pow(abs(tcl - ta), 0.25)
        hc: float = max(hcf, hcr)

        tcl_new: float = 35.7 - 0.028 * mw - icl * (
            3.96e-8 * fcl * (math.pow(tcla, 4) - math.pow(tra, 4)) +
            fcl * hc * (tcl - ta)
        )
        if abs(tcl_new - tcl) < 0.001:
            break
        tcl = tcl_new

    hl1: float = 3.05 * 0.001 * (5733 - 6.99 * mw - pa)
    hl2: float = 0.42 * (mw - 58.15) if mw > 58.15 else 0.0
    hl3: float = 1.7e-5 * m * (5867 - pa)
    hl4: float = 0.0014 * m * (34 - ta)
    hl5: float = 3.96e-8 * fcl * (math.pow(tcl + 273.15, 4) - math.pow(tr + 273.15, 4))
    hl6: float = fcl * hc * (tcl - ta)

    thermal_load: float = mw - (hl1 + hl2 + hl3 + hl4 + hl5 + hl6)
    pmv: float = (0.303 * math.exp(-0.036 * m) + 0.028) * thermal_load
    return round(max(-3.0, min(3.0, pmv)), 3)


class EMSInterface:
    """
    Multi-Zone EMS Interface to manage sensor handles, actuator handles, and read/write callbacks.
    Tracks state across 3 distinct zones: Open_Office, Executive_Suite, and Conference_Room.
    """
    def __init__(self) -> None:
        self.sensor_handles: Dict[str, str] = {}
        self.actuator_handles: Dict[str, str] = {}
        
        self.zones_state: Dict[str, Dict[str, Any]] = {
            "Open_Office": {
                "zone_name": "Open_Office",
                "zone_temp": 22.0,
                "pmv": 0.0,
                "occupancy": 10,
                "cooling_setpoint": 22.5,
                "heating_setpoint": 20.0,
                "lighting_level": 1.0
            },
            "Executive_Suite": {
                "zone_name": "Executive_Suite",
                "zone_temp": 22.0,
                "pmv": 0.0,
                "occupancy": 2,
                "cooling_setpoint": 22.5,
                "heating_setpoint": 20.0,
                "lighting_level": 1.0
            },
            "Conference_Room": {
                "zone_name": "Conference_Room",
                "zone_temp": 22.0,
                "pmv": 0.0,
                "occupancy": 0,
                "cooling_setpoint": 24.0,
                "heating_setpoint": 19.0,
                "lighting_level": 0.5
            }
        }
        
        self.global_state: Dict[str, Any] = {
            "timestep": 0,
            "hour": 0,
            "outdoor_temp": 20.0,
            "energy_so_far": 0.0
        }

    def register_sensors(self, ems_api: Any = None, state: Any = None) -> Dict[str, str]:
        """
        Registers EMS sensor handles for zone air temperatures, outdoor temp, and HVAC energy rate.

        Returns:
            Dict[str, str]: Mapping of sensor key to EMS sensor handle name.
        """
        self.sensor_handles = {
            "zone_temp_open_office": "Open_Office Zone Mean Air Temperature",
            "zone_temp_exec_suite": "Executive_Suite Zone Mean Air Temperature",
            "zone_temp_conf_room": "Conference_Room Zone Mean Air Temperature",
            "outdoor_temp": "Site Outdoor Air Drybulb Temperature",
            "hvac_energy": "Facility Total HVAC Electricity Demand Rate"
        }
        logger.info(f"Registered {len(self.sensor_handles)} EMS sensor handles.")
        return self.sensor_handles

    def register_actuators(self, ems_api: Any = None, state: Any = None) -> Dict[str, str]:
        """
        Registers EMS actuator handles for thermostat cooling setpoints.

        Returns:
            Dict[str, str]: Mapping of actuator key to EMS actuator handle name.
        """
        self.actuator_handles = {
            "open_office_cooling": "Open_Office Cooling Setpoint",
            "exec_suite_cooling": "Executive_Suite Cooling Setpoint",
            "conf_room_cooling": "Conference_Room Cooling Setpoint"
        }
        logger.info(f"Registered {len(self.actuator_handles)} EMS actuator handles.")
        return self.actuator_handles

    def get_all_zone_states(self) -> List[Dict[str, Any]]:
        """
        Returns list of state dictionaries for all building zones.

        Returns:
            List[Dict[str, Any]]: Zone telemetry dictionaries.
        """
        return list(self.zones_state.values())

    def callback_read(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        EMS Read-Only Callback firing every timestep. Updates internal state and returns telemetry.

        Args:
            state (Dict[str, Any]): Input physical state from simulation step.

        Returns:
            Dict[str, Any]: Consolidated telemetry dictionary.
        """
        outdoor_temp: float = state.get("outdoor_temp", self.global_state["outdoor_temp"])
        energy_so_far: float = state.get("energy_so_far", self.global_state["energy_so_far"])
        self.global_state["outdoor_temp"] = outdoor_temp
        self.global_state["energy_so_far"] = energy_so_far

        if "zones" in state:
            for z_name, z_data in state["zones"].items():
                if z_name in self.zones_state:
                    self.zones_state[z_name].update(z_data)
                    self.zones_state[z_name]["pmv"] = calculate_pmv(self.zones_state[z_name]["zone_temp"])
        else:
            main_temp: float = state.get("zone_temp", self.zones_state["Open_Office"]["zone_temp"])
            self.zones_state["Open_Office"]["zone_temp"] = main_temp
            self.zones_state["Open_Office"]["pmv"] = calculate_pmv(main_temp)
            if "occupancy" in state:
                self.zones_state["Open_Office"]["occupancy"] = state["occupancy"]

        primary_zone: Dict[str, Any] = self.zones_state["Open_Office"]
        return {
            "zone_temp": round(primary_zone["zone_temp"], 2),
            "pmv": primary_zone["pmv"],
            "energy_so_far": round(energy_so_far, 3),
            "outdoor_temp": round(outdoor_temp, 2),
            "occupancy": int(primary_zone["occupancy"]),
            "zones": self.get_all_zone_states()
        }

    def apply_action(self, state: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
        """
        EMS Actuator Write-Back function to set zone thermostat cooling and heating setpoints.

        Args:
            state (Dict[str, Any]): Current physical state.
            action (Dict[str, Any]): Action payload containing target zone and setpoint values.

        Returns:
            Dict[str, Any]: Updated zone state dictionary.
        """
        target_zone: str = action.get("zone", "Open_Office")
        c_set: Optional[float] = action.get("cooling_setpoint")
        h_set: Optional[float] = action.get("heating_setpoint")
        l_level: Optional[float] = action.get("lighting_level")

        zones_to_update: List[str] = list(self.zones_state.keys()) if target_zone == "All" else [target_zone]

        for z_name in zones_to_update:
            if z_name in self.zones_state:
                if c_set is not None:
                    self.zones_state[z_name]["cooling_setpoint"] = float(c_set)
                if h_set is not None:
                    self.zones_state[z_name]["heating_setpoint"] = float(h_set)
                if l_level is not None:
                    self.zones_state[z_name]["lighting_level"] = float(l_level)

        logger.debug(f"Applied action to zone {target_zone}: {action}")
        return self.zones_state.get(target_zone, self.zones_state["Open_Office"])

# Global singleton instance
ems_interface_instance: EMSInterface = EMSInterface()

def register_sensors(ems_api: Any = None, state: Any = None) -> Dict[str, str]:
    return ems_interface_instance.register_sensors(ems_api, state)

def register_actuators(ems_api: Any = None, state: Any = None) -> Dict[str, str]:
    return ems_interface_instance.register_actuators(ems_api, state)

def get_all_zone_states() -> List[Dict[str, Any]]:
    return ems_interface_instance.get_all_zone_states()

def callback_read(state: Dict[str, Any]) -> Dict[str, Any]:
    return ems_interface_instance.callback_read(state)

def apply_action(state: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
    return ems_interface_instance.apply_action(state, action)
