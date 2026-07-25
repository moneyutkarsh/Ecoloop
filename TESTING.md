# Eco-Loop Building Agents — Software Quality, Reliability & Failure-Mode Testing Documentation

## Executive Summary
This document records the automated and deliberate failure-mode testing results for the **Eco-Loop Building Agents** system.

---

## 1. Clean-State Full Pipeline Automated Verification (`test_full_pipeline.py`)

A clean-state test harness (`test_full_pipeline.py`) was created to delete pre-existing logs, run baseline and AI simulation loops from scratch, validate data integrity (row counts, column schemas, non-null assertions), and test dashboard application syntax.

### Pipeline Performance Timings
| Pipeline Stage | Action / Test | Duration | Result | Data Integrity Checks |
| :--- | :--- | :---: | :---: | :--- |
| **Stage 1: Log Purge** | Delete pre-existing CSV/JSONL files | 0.05s | `PASS` | Log directory cleaned |
| **Stage 2: Baseline Simulation** | `python src/run_baseline.py` | 1.23s | `PASS` | 96 rows, 0 nulls, 83.80 kWh |
| **Stage 3: Deep Reasoning AI Loop** | `python src/run_ai_loop.py` | 2.27s | `PASS` | 96 rows, 24 decisions, 75.52 kWh |
| **Stage 4: Dashboard App** | `python -m py_compile dashboard/app.py` | 0.17s | `PASS` | Syntax compiled cleanly |
| **TOTAL PIPELINE DURATION** | **End-to-End Clean Verification** | **3.44s** | **`ALL PASS`** | **100% Zero-Crash Verified** |

---

## 2. Deliberate Failure-Mode & Anomaly Resilience Test Suite

| Test Case | Scenario / Injected Condition | Expected Behavior | Actual Behavior | Result |
| :--- | :--- | :--- | :--- | :---: |
| **TC-01: Ollama Server Offline** | Ollama HTTP endpoint connection refused (`localhost:11434`) | Fallback to internal physics-informed heuristic reasoning engine without hanging or crashing | Caught connection error, applied rule-based pre-cooling & setback actions safely | `PASS` |
| **TC-02: Missing Weather File** | `models/weather.epw` deleted or corrupted | System catches missing file, logs clear warning, and uses built-in EPW diurnal fallback curve | Loaded 24-hour diurnal weather profile (21.5°C to 33.0°C) with zero crashes | `PASS` |
| **TC-03: Malformed LLM Tool Response** | Unparseable JSON tool payload injected at Step 48 (12:00) | Catch JSON error, log `event_type: malformed_llm_response`, apply safe cooling setpoint (22.5°C) | Logged fallback event, setpoint held at 22.5°C, simulation continued smoothly | `PASS` |
| **TC-04: Sensor Fault Anomaly Spike** | Temperature sensor fault (52.0°C spike in Conference Room) at Step 36 (09:00) | Flag `flagged_anomaly = True`, drop confidence to 0.30, apply safe fallback (22.5°C) | Detected physical impossibility (>45°C), applied safety override, zero comfort violation | `PASS` |
| **TC-05: Cross-Platform Portability Audit** | Hardcoded machine paths check across `src/*.py` | All path references anchored relative to `BASE_DIR = Path(__file__).resolve().parent.parent` | All paths dynamic & portable across Windows, macOS, and Linux | `PASS` |

---

## 3. Automated Unit Test Suite (`tests/test_bms.py`)

Run command: `python tests/test_bms.py`

- `[OK] test_config_validation` — Verified configuration constants & bounds.
- `[OK] test_pmv_calculation_reference_values` — Verified Fanger PMV calculation against ISO 7730 standards.
- `[OK] test_carbon_signal_ranges` — Verified grid carbon profile bounds (180 to 420 gCO2/kWh).
- `[OK] test_lookahead_forecast` — Verified 2-hour lookahead window accuracy.
- `[OK] test_anomaly_fault_detection` — Verified sensor fault override logic.
- `[OK] test_memory_summarization` — Verified episodic memory summarization.
- `[OK] test_malformed_llm_response_recovery` — Verified malformed LLM tool call recovery.

---

## 4. Verification Command
To run all tests and verify the complete harness:
```bash
python test_full_pipeline.py --force
python tests/test_bms.py
```
