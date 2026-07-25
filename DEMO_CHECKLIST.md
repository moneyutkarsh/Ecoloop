# Eco-Loop Building Agents — Hackathon Live Presentation & Demo Checklist

## Executive Summary
This checklist provides step-by-step instructions, pre-presentation setup commands, expected timings, and fallback contingencies for demonstrating the **Eco-Loop Building Agents** system during the live presentation pitch.

---

## ⏱️ Performance Benchmarks & Timings

| Execution Stage | Command | Wall-Clock Duration | Target Output |
| :--- | :--- | :---: | :--- |
| **1. Full Pipeline Verification** | `python test_full_pipeline.py --force` | **3.44s** | Purges logs & validates baseline + AI loop |
| **2. Automated Test Suite** | `python tests/test_bms.py` | **0.85s** | All 7 unit tests pass |
| **3. Baseline Simulation** | `python src/run_baseline.py` | **1.23s** | Creates `logs/baseline_output.csv` (83.80 kWh) |
| **4. AI Control Loop** | `python src/run_ai_loop.py` | **1.99s** | Creates `logs/ai_output.csv` & `decisions_log.jsonl` |
| **5. Live Dashboard** | `streamlit run dashboard/app.py` | **< 1.00s load** | Browser opens at `http://localhost:8501` |

---

## 📋 Pre-Presentation Setup Checklist (Run 5 Minutes Before Pitch)

### Step 1: Clean & Run Full Pipeline
Open terminal in the project directory (`Eco-Building Agent`) and execute:
```bash
python test_full_pipeline.py --force
```
- Verify output ends with `SUMMARY: ALL PIPELINE TESTS PASSED 100% SUCCESSFULLY`.

### Step 2: Launch Presentation Dashboard
Execute:
```bash
streamlit run dashboard/app.py
```
- Verify browser opens to `http://localhost:8501`.
- Verify top status pill displays: `🟢 SIMULATION COMPLETE | 24 AI DECISIONS | 2 STRESS TESTS HANDLED`.

---

## 🎤 3-Minute Live Pitch Walkthrough Strategy

### 1. Executive Summary & Hero Savings (0:00 - 0:45)
- Point to top **Hero Summary Banner**:
  > *"Eco-Loop AI reduced HVAC energy by 9.9% and grid carbon emissions by 14.2% while maintaining 100% thermal comfort compliance under ISO 7730 standards."*
- Point to the **5 Metric Cards**:
  - `+9.9%` HVAC Energy Saved
  - `75.52 kWh` Total Energy
  - `3.32 kg` CO2 Offset
  - `100%` Comfort Compliance
  - `2` Stress Tests Handled

### 2. Deep 4-Step Reasoning & Counterfactual Inspector (0:45 - 1:45)
- Click **Tab 2: `🧠 Deep Reasoning & 4-Step Chain Inspector`**.
- Drag the **Step Slider** to **Step 9 (09:00 - Sensor Fault Anomaly)**:
  - Show how the agent caught the `52.0°C` corrupted reading, lowered confidence to `0.30`, and safely held setpoint at `22.5°C`.
- Drag the **Step Slider** to **Step 12 (12:00 - Malformed Response Recovery)**:
  - Show how the agent caught the unparseable tool call payload, logged `event_type: malformed_llm_response`, and recovered automatically with zero downtime.
- Show the **4-Step Reasoning Chain**:
  - `1. ASSESS` → `2. FORECAST` (2H lookahead) → `3. TRADEOFF` → `4. DECIDE`.
- Show the **Counterfactual Analysis Box**:
  - Explains what action was considered and why it was rejected.

### 3. Model Context Protocol (MCP) & System Internals (1:45 - 2:30)
- Click **Tab 3: `📁 Telemetry, MCP & System Internals`**.
- Expand **`🔍 View JSON Tool Schema`**:
  - Show MCP JSON-RPC tool schemas (`get_zone_state`, `set_thermostat_setpoint`).

### 4. Optional Live Streaming Demonstration (2:30 - 3:00)
- In Tab 1, check `🔴 Enable Live Real-Time File Streaming (2s Auto-Refresh)`.
- In a second terminal, execute `python src/run_ai_loop.py` to demonstrate decisions appearing live on screen!

---

## 🛡️ Fallback & Contingency Plan

If live execution or network connectivity issues occur during the pitch:
1. **Offline Replay Mode**: In Tab 1, check `▶ Enable Offline Replay Mode` and drag the playhead slider to demonstrate simulated real-time play.
2. **Local Heuristic Engine**: The system runs 100% locally without cloud API keys, guaranteeing zero downtime.
