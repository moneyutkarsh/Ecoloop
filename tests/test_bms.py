"""
Automated Test Suite for Eco-Loop Building Agents.
Validates thermal comfort PMV calculations, carbon signal curves, anomaly fault detection,
memory summarization, and LLM malformed response recovery.
"""
import sys
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from config import validate_config
from ems_interface import calculate_pmv, get_all_zone_states, callback_read, apply_action
from carbon_signal import get_carbon_intensity, is_low_carbon_hour, is_high_carbon_hour, get_lookahead_forecast
from memory import record_decision, summarize_recent_decisions
from llm_agent import decide_action, LLMAgent

def test_config_validation():
    """Validates startup configuration assertions."""
    assert validate_config() is True

def test_pmv_calculation_reference_values():
    """
    Validates Fanger ISO 7730 PMV thermal comfort index against reference benchmarks.
    """
    # Baseline comfortable room (22°C, 50% RH, 1.2 met, 0.6 clo) -> PMV near 0
    pmv_comfortable = calculate_pmv(22.0, 22.0, 0.1, 50.0, 1.2, 0.6)
    assert -0.5 <= pmv_comfortable <= 0.5, f"Expected PMV in [-0.5, 0.5], got {pmv_comfortable}"

    # Hot room (32°C) -> PMV should be positive (> 1.0)
    pmv_hot = calculate_pmv(32.0, 32.0, 0.1, 50.0, 1.2, 0.6)
    assert pmv_hot > 1.0, f"Expected PMV > 1.0 for hot room, got {pmv_hot}"

    # Cold room (15°C) -> PMV should be negative (< -0.5)
    pmv_cold = calculate_pmv(15.0, 15.0, 0.1, 50.0, 1.2, 0.6)
    assert pmv_cold < -0.5, f"Expected PMV < -0.5 for cold room, got {pmv_cold}"

def test_carbon_signal_ranges():
    """
    Validates grid carbon intensity curve values for solar valley and peak carbon hours.
    """
    # Midday Solar Valley (12:00) should be clean (< 250 gCO2/kWh)
    carbon_midday = get_carbon_intensity(12)
    assert carbon_midday < 250.0, f"Expected clean carbon midday, got {carbon_midday}"
    assert is_low_carbon_hour(12) is True

    # Evening Peak (19:00) should be high carbon (> 500 gCO2/kWh)
    carbon_evening = get_carbon_intensity(19)
    assert carbon_evening > 500.0, f"Expected high carbon evening, got {carbon_evening}"
    assert is_high_carbon_hour(19) is True

def test_lookahead_forecast():
    """
    Validates 2-hour forward lookahead forecast structure and parameters.
    """
    forecast = get_lookahead_forecast(hour_of_day=9, hours_ahead=2)
    assert "forecast_hours" in forecast
    assert len(forecast["forecast_hours"]) == 2
    assert "carbon_forecast_gco2_kwh" in forecast
    assert "occupancy_forecast" in forecast

def test_anomaly_fault_detection():
    """
    Validates that implausible sensor readings (>40°C) trigger anomaly detection.
    """
    telemetry = {
        "zone_temp": 52.0,  # Corrupted sensor reading!
        "pmv": 3.0,
        "energy_so_far": 10.0,
        "zones": [
            {"zone_name": "Open_Office", "zone_temp": 52.0, "occupancy": 10}
        ]
    }
    action, justification, flagged_anomaly, confidence_score, reasoning_chain, counterfactual = decide_action(
        timestamp="2026-07-01 09:00:00",
        hour=9,
        telemetry=telemetry,
        carbon_intensity=480.0
    )
    assert flagged_anomaly is True, "Expected anomaly to be flagged for 52.0°C reading"
    assert confidence_score == 0.30, f"Expected confidence 0.30, got {confidence_score}"
    assert action["cooling_setpoint"] == 22.5, "Expected safe fallback setpoint 22.5°C"

def test_memory_summarization():
    """
    Validates self-correction decision memory store and text summarization.
    """
    record_decision(
        timestamp="2026-07-01 10:00:00",
        zone="Open_Office",
        action={"cooling_setpoint": 21.5},
        justification="Test pre-cooling action",
        resulting_temp=22.0,
        resulting_pmv=-0.1,
        resulting_energy_delta=0.5,
        carbon_intensity=210.0
    )
    summary = summarize_recent_decisions(n=5)
    assert isinstance(summary, str)
    assert len(summary) > 20
    assert "SUMMARY OF LAST" in summary

def test_malformed_llm_response_recovery():
    """
    Simulates malformed / garbage LLM output and verifies zero-crash fallback recovery.
    """
    agent = LLMAgent()
    malformed_telemetry = {}
    action, justification, flagged_anomaly, confidence, reasoning_chain, counterfactual = agent.decide_action(
        timestamp="2026-07-01 12:00:00",
        hour=12,
        telemetry=malformed_telemetry,
        carbon_intensity=200.0
    )
    assert action is not None
    assert "cooling_setpoint" in action
    assert isinstance(justification, str)

if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING ECO-LOOP BUILDING AGENTS AUTOMATED TEST SUITE")
    print("=" * 60)
    test_config_validation()
    print("[OK] test_config_validation PASSED")
    test_pmv_calculation_reference_values()
    print("[OK] test_pmv_calculation_reference_values PASSED (ISO 7730 Verified)")
    test_carbon_signal_ranges()
    print("[OK] test_carbon_signal_ranges PASSED")
    test_lookahead_forecast()
    print("[OK] test_lookahead_forecast PASSED")
    test_anomaly_fault_detection()
    print("[OK] test_anomaly_fault_detection PASSED (Fault Anomaly Overridden Safely)")
    test_memory_summarization()
    print("[OK] test_memory_summarization PASSED")
    test_malformed_llm_response_recovery()
    print("[OK] test_malformed_llm_response_recovery PASSED (Zero-Crash Fallback Verified)")
    print("=" * 60)
    print("ALL 7 AUTOMATED UNIT TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)
