"""
Self-Correction Memory Module (Phase 6).
Maintains a rolling window of recent AI decisions and resulting building telemetry outcomes,
producing concise text summaries for LLM prompt injection to enable self-correction.
"""
import json
import logging
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class DecisionMemory:
    """
    Rolling memory store for AI decisions and self-correction.
    """
    def __init__(self, max_history: int = 20):
        self.max_history = max_history
        self.history: List[Dict[str, Any]] = []

    def record_decision(
        self,
        timestamp: str,
        zone: str,
        action: Dict[str, Any],
        justification: str,
        resulting_temp: float,
        resulting_pmv: float,
        resulting_energy_delta: float,
        carbon_intensity: float
    ):
        """
        Records a decision cycle into rolling memory.
        """
        entry = {
            "timestamp": timestamp,
            "zone": zone,
            "action": action,
            "justification": justification,
            "resulting_temp": resulting_temp,
            "resulting_pmv": resulting_pmv,
            "resulting_energy_delta": resulting_energy_delta,
            "carbon_intensity": carbon_intensity
        }
        self.history.append(entry)
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def summarize_recent_decisions(self, n: int = 5) -> str:
        """
        Summarizes the last n decisions and their thermal/energy outcomes into a concise string.
        Highlights any comfort violations or high-carbon energy usage to guide self-correction.
        """
        if not self.history:
            return "No previous decisions recorded yet. Operating at default baseline state."

        recent = self.history[-n:]
        summary_lines = []
        comfort_violations = 0
        setback_actions = 0
        pre_cooling_actions = 0

        for idx, d in enumerate(recent, 1):
            pmv = d.get("resulting_pmv", 0.0)
            temp = d.get("resulting_temp", 22.0)
            action = d.get("action", {})
            c_set = action.get("cooling_setpoint", 22.5)
            h_set = action.get("heating_setpoint", 20.0)
            carbon = d.get("carbon_intensity", 350.0)
            justification = d.get("justification", "Regular adjustment")

            # Check comfort violation (PMV outside [-0.5, +0.5])
            if pmv > 0.5:
                comfort_violations += 1
                status = f"⚠️ COMFORT OVERHEAT RISK (PMV = +{pmv:.2f} > +0.5 at {temp:.1f}°C)"
            elif pmv < -0.5:
                comfort_violations += 1
                status = f"⚠️ COMFORT OVERCOOL RISK (PMV = {pmv:.2f} < -0.5 at {temp:.1f}°C)"
            else:
                status = f"✅ COMFORT OPTIMAL (PMV = {pmv:+.2f})"

            if c_set > 23.5:
                setback_actions += 1
            elif c_set < 22.0:
                pre_cooling_actions += 1

            summary_lines.append(
                f"- T-{idx} [{d['timestamp'][-8:-3]}]: Set cooling to {c_set:.1f}°C. Outcome: Temp={temp:.1f}°C, {status}. Carbon={carbon:.0f} g/kWh."
            )

        header = f"SUMMARY OF LAST {len(recent)} DECISIONS:"
        if comfort_violations > 0:
            guidance = f"CRITICAL GUIDANCE: {comfort_violations} of last {len(recent)} actions caused comfort threshold warnings! Tighten cooling setpoint to protect occupant comfort."
        elif pre_cooling_actions > 0:
            guidance = "GUIDANCE: Pre-cooling strategy active. Ensure setpoints transition smoothly before peak carbon hours."
        elif setback_actions > 0:
            guidance = "GUIDANCE: Energy setback active. Monitor PMV to ensure room does not exceed 24.5°C."
        else:
            guidance = "GUIDANCE: System operating stably within optimal comfort bounds."

        return header + "\n" + "\n".join(summary_lines) + "\n" + guidance

# Global memory instance
memory_instance = DecisionMemory()

def record_decision(timestamp, zone, action, justification, resulting_temp, resulting_pmv, resulting_energy_delta, carbon_intensity):
    memory_instance.record_decision(timestamp, zone, action, justification, resulting_temp, resulting_pmv, resulting_energy_delta, carbon_intensity)

def summarize_recent_decisions(n: int = 5) -> str:
    return memory_instance.summarize_recent_decisions(n)
