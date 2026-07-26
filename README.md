# Eco-Loop Building Agents

> Autonomous, carbon-aware building management system pairing EnergyPlus digital twins with LLMs and the Model Context Protocol (MCP).

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](test_full_pipeline.py)
[![Protocol: MCP](https://img.shields.io/badge/protocol-MCP--JSON--RPC-purple.svg)](src/mcp_server.py)
[![Physics: EnergyPlus](https://img.shields.io/badge/physics-EnergyPlus--24.1-orange.svg)](models/baseline_doe_reference.idf)
[![Comfort: ISO 7730](https://img.shields.io/badge/comfort-ISO--7730-green.svg)](docs/architecture.md)

![Eco-Loop Overview](ScreenShots/Screenshot%202026-07-26%20164237.png)

---

## Table of Contents

- [About the Project](#about-the-project)
- [Why This Matters](#why-this-matters)
- [Key Features](#key-features)
- [Performance Results](#performance-results)
- [Architecture Diagram](#architecture-diagram)
- [How the Closed Loop Works](#how-the-closed-loop-works)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Running the Demo](#running-the-demo)
- [Repository Walkthrough](#repository-walkthrough)
- [Engineering Validation](#engineering-validation)
- [Standards Compliance](#standards-compliance)
- [Testing](#testing)
- [Results](#results)
- [Artifacts](#artifacts)
- [Future Work](#future-work)
- [Contributors](#contributors)
- [License](#license)

---

## About the Project

**Eco-Loop Building Agents** is an open-source, closed-loop Building Management System (BMS). It integrates physics-based building simulation (via the EnergyPlus EMS API) with an autonomous Large Language Model agent (Ollama / Llama 3.1 / Qwen 2.5) using the Model Context Protocol (MCP).

The system replaces static, rule-based thermostat schedules with dynamic closed-loop control. It continuously evaluates real-time thermal comfort (ISO 7730 PMV), 2-hour forward-looking weather, occupancy schedules, and marginal grid carbon intensity (EIA-930 PJM ComEd) to optimize HVAC setpoints without human intervention.

---

## Why This Matters

Commercial buildings account for a significant share of global electricity demand and grid peak loads. Conventional BMS platforms operate on static schedules:

- **Static Setpoints**: Maintain fixed cooling setpoints regardless of grid carbon intensity or dynamic occupancy.
- **No Forward Awareness**: Lack predictive pre-cooling during low-carbon generation windows.
- **Siloed Execution**: Lack standardized tool-calling interfaces to integrate predictive AI models safely.

Eco-Loop resolves these limitations by establishing a standardized, closed-loop control architecture that couples building energy simulation directly to autonomous LLM decision agents while maintaining strict safety constraints and thermal comfort boundaries.

---

## Key Features

- **✔ EnergyPlus Digital Twin**: Native integration with the U.S. DOE Commercial Reference Building (`RefBldgSmallOfficeNew2004_Chicago.idf`).
- **✔ Autonomous HVAC Optimization**: Dynamic 15-minute closed-loop setpoint adjustment across multi-zone office topologies.
- **✔ Explainable AI Reasoning**: Auditable 4-stage decision chain (`ASSESS ➔ FORECAST ➔ TRADEOFF ➔ DECIDE`) with per-timestep counterfactual logging.
- **✔ Carbon-Aware Scheduling**: Pre-cools during low-carbon windows (<250 gCO₂/kWh) and curtails load during grid carbon peaks (>500 gCO₂/kWh).
- **✔ MCP Tool Calling**: Standardized JSON-RPC 2.0 tool interface (`get_zone_state`, `get_carbon_intensity`, `set_thermostat_setpoint`).
- **✔ Safety Validation**: Deterministic rule-engine bounds setpoint changes within ISO 7730 thermal comfort boundaries `[-0.5, +0.5]`.
- **✔ Fault Recovery**: Defensive anomaly handling overrides physical sensor noise spikes (e.g., 52°C) and malformed LLM responses cleanly.
- **✔ Live Dashboard**: Real-time Streamlit control center featuring an animated SVG Digital Twin, occupancy heatmaps, and telemetry exports.

---

## Performance Results

All metrics are verified through automated pipeline execution (`python test_full_pipeline.py --force`) over a 24-hour simulation period (96 timesteps):

| Metric | Unmodified DOE Baseline | Eco-Loop Autonomous | Savings / Improvement | Verification Source |
| :--- | :---: | :---: | :---: | :--- |
| **Total HVAC Energy** | `83.80 kWh` | **`75.52 kWh`** | **`+9.9% Energy Saved`** (8.28 kWh) | EnergyPlus EMS Telemetry |
| **Grid Carbon Footprint** | `23.35 kg CO2` | **`20.02 kg CO2`** | **`+14.2% CO2 Offset`** (3.33 kg) | EIA-930 PJM Historical Data |
| **Thermal Comfort (PMV)** | `0 Violations` | **`0 Violations`** | **`100.0% ISO Compliance`** | Fanger PMV inside `[-0.5, +0.5]` |
| **Annualized HVAC EUI** | `59.8 kWh/m²/yr` | **`53.9 kWh/m²/yr`** | **`5.9 kWh/m²/yr EUI`** | Validated against DOE CBECS |
| **Annual Cost Savings** | `$0` | **`$10,883 / yr`** | **`$10,883 / yr`** | Scaled to 5,000 m² office ($0.15/kWh) |
| **System Reliability** | `N/A` | **`2 Fault Events`** | **`100% Zero-Crash`** | Sensor noise & LLM payload fallback |

---

## Architecture Diagram

![System Architecture](ScreenShots/Screenshot%202026-07-26%20164321.png)

```
[EnergyPlus Digital Twin] ──(EMS Telemetry)──► [TelemetryStreamGateway]
                                                      │
[EIA-930 Grid & EPW Data] ──(2H Lookahead)────► [MCP Server Engine]
                                                      │
[Decision Memory Buffer] ──(Rolling Context)──► [LLM Agent (Ollama/Llama 3.1)]
                                                      │ (4-Stage Reasoning)
                                                      ▼
[EnergyPlus EMS Actuator] ◄──(Safe Bounds)───── [Deterministic Rule Engine]
```

---

## How the Closed Loop Works

1. **Telemetry Ingestion**: Every 15 minutes, `ems_interface.py` captures zone dry-bulb temperatures, mean radiant temperatures, relative humidity, and occupant counts.
2. **Signal & Forecast Aggregation**: `carbon_signal.py` queries current and 2-hour forward-looking PJM ComEd grid carbon intensity alongside outdoor weather forecasts.
3. **MCP Tool Calling**: The LLM agent receives telemetry via `src/mcp_server.py` and evaluates comfort, energy, and carbon trade-offs.
4. **Reasoning & Safety Validation**: The agent generates an auditable 4-stage reasoning chain (`ASSESS ➔ FORECAST ➔ TRADEOFF ➔ DECIDE`). Proposed setpoints are passed to a deterministic rule engine to ensure compliance with ISO 7730 PMV bounds `[-0.5, +0.5]`.
5. **Actuator Execution**: Validated cooling, heating, and lighting setpoints are written back to EnergyPlus EMS actuators.

---

## Technology Stack

- **Physics Simulation**: EnergyPlus 24.1 / `pyenergyplus` EMS API
- **AI & Agent Protocol**: Python 3.10+ / Model Context Protocol (MCP) / Ollama (Llama 3.1, Qwen 2.5)
- **Data & Signal Processing**: Pandas, NumPy, EIA-930 PJM ComEd historical grid carbon dataset
- **User Interface**: Streamlit, Altair, HTML5/CSS3 glassmorphism design system
- **Testing Harness**: Pytest, automated data lineage verification

---

## Project Structure

```
eco-loop-building-agents/
├── README.md                     # Master documentation
├── BENCHMARKS.md                 # Single source-of-truth verified metrics
├── TESTING.md                    # Software quality & failure-mode docs
├── DEMO_CHECKLIST.md             # Hackathon presentation walkthrough
├── requirements.txt              # Dependency manifest
├── run_full_demo.py              # One-command demo launcher
├── test_full_pipeline.py         # Verification test harness
│
├── dashboard/
│   └── app.py                    # Streamlit Enterprise Control Center UI
│
├── src/
│   ├── ems_interface.py          # EMS sensors, actuators & ISO 7730 PMV engine
│   ├── carbon_signal.py          # Real EIA-930 PJM grid emissions & forecast module
│   ├── llm_agent.py              # Predictive tool-calling LLM agent & anomaly engine
│   ├── memory.py                 # Self-correction decision memory buffer
│   ├── run_baseline.py           # Unmodified baseline simulation runner
│   ├── run_ai_loop.py            # Autonomous closed-loop AI simulation runner
│   ├── mcp_server.py             # Model Context Protocol (MCP) JSON-RPC server
│   ├── telemetry_stream.py       # Hardware-agnostic pub/sub ingestion gateway
│   ├── schemas.py                # Sensor & action payload JSON schemas
│   └── config.py                 # Thermal bounds & startup validation layer
│
├── models/
│   ├── baseline_doe_reference.idf # Official DOE Small Office Reference Model
│   ├── baseline_custom.idf        # Preserved baseline fallback model
│   └── weather.epw               # Chicago O'Hare TMY3 weather dataset
│
├── tests/
│   ├── test_bms.py               # Pytest unit test suite (7/7 unit tests)
│   └── test_data_lineage.py      # Data provenance verification suite
│
├── logs/
│   ├── baseline_output.csv       # Baseline simulation telemetry
│   ├── ai_output.csv             # AI closed-loop simulation telemetry
│   └── decisions_log.jsonl       # JSON-RPC decision reasoning & anomaly log
│
└── ScreenShots/                  # UI dashboard screenshots
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/moneyutkarsh/Ecoloop.git
cd Ecoloop

# Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Quick Start

Run the automated pipeline test harness to verify setup:

```bash
python test_full_pipeline.py --force
```

**Expected Output:**
```
======================================================================
  SUMMARY: ALL PIPELINE TESTS PASSED 100% SUCCESSFULLY
======================================================================
  1. Baseline Simulation:   1.24s  [PASS]
  2. Deep Reasoning AI:     2.06s  [PASS]
  3. Dashboard App Syntax:  0.19s  [PASS]
  4. BMS Unit Test Suite:   2.49s  [PASS]
  -------------------------------------------
  TOTAL PIPELINE TIMING:    5.98s  [ALL PASS]
```

---

## Running the Demo

Launch the end-to-end pipeline and interactive dashboard with a single command:

```bash
python run_full_demo.py
```

Open **`http://localhost:8501`** in your browser to view the live Control Center UI.

---

## Repository Walkthrough

> Select a section below to expand detailed documentation.

<details>
<summary>📸 Dashboard UI Gallery & Workspaces</summary>

### Live Control Center
![Control Center Dashboard](ScreenShots/Screenshot%202026-07-26%20164332.png)

### Performance & Playback Timeline
![Performance Playback](ScreenShots/Screenshot%202026-07-26%20164347.png)

### Deep Reasoning Inspector
![Reasoning Inspector](ScreenShots/Screenshot%202026-07-26%20164356.png)

### Financial & Environmental ROI Calculator
![ROI Calculator](ScreenShots/Screenshot%202026-07-26%20164410.png)

### MCP Sandbox & Telemetry Stream
![MCP Sandbox](ScreenShots/Screenshot%202026-07-26%20164428.png)

</details>

<details>
<summary>📐 Thermal Comfort Derivation (ISO 7730 Fanger PMV)</summary>

Thermal comfort is computed at each timestep using the Fanger PMV energy balance model:

$$\text{PMV} = (0.303 e^{-0.036 M} + 0.028) \times \left[ (M - W) - H_{\text{skin}} - H_{\text{resp}} - H_{\text{rad}} - H_{\text{conv}} \right]$$

**Parameters:**
- $T_{db}$: Air dry-bulb temperature (°C)
- $T_r$: Mean radiant temperature (°C)
- $v$: Air velocity ($0.1\text{ m/s}$)
- $RH$: Relative humidity (%)
- $M$: Metabolic rate ($1.2\text{ met}$ / office work)
- $I_{cl}$: Clothing insulation ($0.6\text{ clo}$ / summer attire)

**Comfort Enclosure:** Setpoint decisions are constrained to guarantee $-0.5 \le \text{PMV} \le +0.5$.

</details>

<details>
<summary>🔌 MCP JSON-RPC 2.0 Tool Specifications</summary>

```json
{
  "tools": [
    {
      "name": "get_zone_state",
      "description": "Returns zone dry-bulb temperature, relative humidity, PMV index, and occupancy.",
      "inputSchema": { "type": "object", "properties": { "zone_name": { "type": "string" } }, "required": ["zone_name"] }
    },
    {
      "name": "get_carbon_intensity",
      "description": "Queries historical PJM ComEd grid carbon intensity (gCO2/kWh) for specified hour.",
      "inputSchema": { "type": "object", "properties": { "hour": { "type": "integer" } }, "required": ["hour"] }
    },
    {
      "name": "set_thermostat_setpoint",
      "description": "Applies cooling and heating setpoint bounds to target zone.",
      "inputSchema": { "type": "object", "properties": { "zone_name": { "type": "string" }, "cooling_temp": { "type": "number" }, "heating_temp": { "type": "number" } }, "required": ["zone_name", "cooling_temp", "heating_temp"] }
    }
  ]
}
```

</details>

<details>
<summary>🛡️ Defensive Fault Injection & Anomaly Resilience</summary>

The system handles live operational anomalies cleanly:

1. **Physical Sensor Spike (Step 36 / 09:00)**:
   - *Event*: Corrupted sensor temperature (`52.0°C`) is received.
   - *Recovery*: Anomaly detector flags `flagged_anomaly: True`, drops confidence score to `0.30`, and overrides setpoint to safe fallback (`22.5°C`).
2. **Malformed LLM Output (Step 48 / 12:00)**:
   - *Event*: Unparseable JSON output emitted by LLM.
   - *Recovery*: Exception caught, default baseline setpoint applied without crashing simulation loop.

</details>

---

## Engineering Validation

- **Energy Use Intensity (EUI)**: Annualized HVAC EUI of **53.9 kWh/m²/yr** falls within the U.S. DOE CBECS benchmark range of **50.0–90.0 kWh/m²/yr** for small commercial offices.
- **Hardware-Agnostic Ingestion**: `TelemetryStreamGateway` (`src/telemetry_stream.py`) decouples EnergyPlus simulation from agent logic via standardized pub/sub payload schemas (`SensorTelemetryPayload` / `ActionDecisionPayload`), enabling direct migration to BACnet IP or Modbus TCP hardware controllers.

---

## Standards Compliance

| Standard / Protocol | Domain | Compliance Level |
| :--- | :--- | :--- |
| **ASHRAE Standard 90.1-2004** | Building Energy Baseline | Fully Compliant (DOE Small Office archetype) |
| **ASHRAE Standard 62.1** | Ventilation & IAQ | Fully Compliant (Zone diversity schedules) |
| **ISO 7730 / ASHRAE 55** | Thermal Comfort Index | 100.0% Compliant (0 PMV breaches outside `[-0.5, +0.5]`) |
| **Model Context Protocol (MCP)** | Agent Tool-Calling | JSON-RPC 2.0 Standard Compliant over STDIO |
| **EIA-930 / PJM EIS** | Grid Carbon Data | Real Marginal Emissions (Chicago, IL, July 1, 2024) |
| **DOE CBECS Benchmark** | Energy Use Intensity | Validated (53.9 kWh/m²/yr vs 50–90 kWh/m²/yr baseline) |

---

## Testing

Run unit tests via Pytest:

```bash
python tests/test_bms.py
```

**Test Coverage:**
- `test_config_validation`: Validates startup thermal bounds.
- `test_pmv_calculation_reference_values`: Validates Fanger PMV math against ISO 7730 reference benchmarks.
- `test_carbon_signal_ranges`: Validates grid carbon intensity curve lookup.
- `test_lookahead_forecast`: Validates 2-hour lookahead forecast.
- `test_anomaly_fault_detection`: Validates sensor fault detection and safe fallback override.
- `test_memory_summarization`: Validates decision memory buffer summarization.
- `test_malformed_llm_response_recovery`: Validates zero-crash fallback on unparseable LLM output.

---

## Results

![Key Benchmarks](ScreenShots/Screenshot%202026-07-26%20164531.png)
![Telemetry Analytics](ScreenShots/Screenshot%202026-07-26%20164547.png)

- **HVAC Energy Saved**: `8.28 kWh` (**+9.9% Reduction**)
- **Carbon Emitted Avoided**: `3.33 kg CO2` (**+14.2% Offset**)
- **ISO 7730 Comfort Compliance**: **100.0%** (0 breaches)
- **Zero-Crash Fault Recovery**: **100%** (2/2 stress events handled)

---


## Future Work

- **Multi-Day Horizon Expansion**: Extending closed-loop control across multi-week seasonal weather datasets.
- **Physical BACnet/Modbus Gateway Integration**: Direct deployment to physical IoT building gateways via `TelemetryStreamGateway`.
- **Multi-Building Campus Coordination**: Scaled MCP tool orchestration across heterogeneous building fleets.

---

## Contributors

- **Eco-Loop Engineering Team**

---

## License

This project is licensed under the [MIT License](LICENSE).
