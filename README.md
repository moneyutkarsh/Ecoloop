# ⚡ Eco-Loop Building Agents

> **Autonomous Smart Building Optimization Platform**  
> An autonomous, predictive Building Management System (BMS) that pairs the official **U.S. Department of Energy (DOE) Commercial Reference Building** model (`RefBldgSmallOfficeNew2004_Chicago.idf` via pyenergyplus EMS API) with an open-source Large Language Model (**Ollama / Llama 3.1 / Qwen 2.5**) and the **Model Context Protocol (MCP)**.

---

## 🌟 Key Performance Benchmarks & Results

| Metric | Unmodified DOE Baseline | Eco-Loop AI Autonomous | Improvement |
| :--- | :---: | :---: | :---: |
| **Total HVAC Energy** | `83.80 kWh` | **`75.52 kWh`** | **`+9.9% Energy Savings`** |
| **Grid Carbon Footprint** | `23.35 kg CO2` | **`20.02 kg CO2`** | **`+14.2% CO2 Offsets`** |
| **Comfort Violations (PMV)** | `0` | **`0`** | **`100.0% ISO 7730 Compliance`** |
| **Stress Anomalies Handled** | `0` | **`2 Fault Events`** | **`100% Zero-Crash Resilient`** |

---

## 🏛️ Standards & Building Foundation
- **DOE Reference Model**: Based on PNNL/NREL CBECS survey data for a Small Commercial Office (511 m² / 5,500 ft²) under ASHRAE Standard 90.1-2004.
- **ASHRAE 90.1 / 62.1 Compliance**: Verified occupancy densities (`0.10` people/m² open office, `0.04` people/m² executive suite) and operating diversity schedules.

---

## 🛠️ Project Layout

```
eco-loop-building-agents/
├── models/
│   ├── baseline_doe_reference.idf # Official DOE Small Office Reference Model (ASHRAE 90.1)
│   ├── baseline_custom.idf        # Preserved baseline fallback model
│   └── weather.epw               # Chicago EPW weather dataset
├── src/
│   ├── ems_interface.py          # EMS sensors, actuators & ISO 7730 PMV engine
│   ├── carbon_signal.py          # Carbon curve & 2-hour predictive forecast
│   ├── llm_agent.py              # Predictive tool-calling agent with anomaly detection
│   ├── memory.py                 # Rolling self-correction decision history
│   ├── run_baseline.py           # Multi-zone baseline simulation runner
│   ├── run_ai_loop.py            # Autonomous closed-loop AI simulation runner
│   ├── mcp_server.py             # Model Context Protocol (MCP) Server wrapper
│   ├── telemetry_stream.py       # Hardware-agnostic real-time pub/sub gateway
│   └── config.py                 # Thermal comfort bounds, setpoints & startup validator
├── tests/
│   ├── test_bms.py               # Automated pytest unit test suite
│   └── test_data_lineage.py      # 26/26 data provenance & lineage verification tests
├── logs/
│   ├── baseline_output.csv       # Baseline simulation telemetry
│   ├── ai_output.csv             # AI closed-loop simulation telemetry
│   └── decisions_log.jsonl       # JSON-RPC LLM decision records & anomaly flags
## 📄 Executive Summary & Full Documentation

- **One-Page Executive Summary**: [`EXECUTIVE_SUMMARY.md`](file:///c:/Users/Utkarsh%20Dubey/.gemini/antigravity/Eco-Building%20Agent/EXECUTIVE_SUMMARY.md) (60-second read)
- **Frontend UI & Design System Documentation**: [`docs/FRONTEND_UI_DOCUMENTATION.md`](file:///c:/Users/Utkarsh%20Dubey/.gemini/antigravity/Eco-Building%20Agent/docs/FRONTEND_UI_DOCUMENTATION.md)
- **Master End-to-End Documentation**: [`docs/COMPLETE_SYSTEM_DOCUMENTATION.md`](file:///c:/Users/Utkarsh%20Dubey/.gemini/antigravity/Eco-Building%20Agent/docs/COMPLETE_SYSTEM_DOCUMENTATION.md)
- **Architecture & Evaluation Mapping**: [`docs/architecture.md`](file:///c:/Users/Utkarsh%20Dubey/.gemini/antigravity/Eco-Building%20Agent/docs/architecture.md)

---

## 🛠️ Project Layout

```
eco-loop-building-agents/
├── EXECUTIVE_SUMMARY.md          # One-page 60-second executive summary
├── models/
│   ├── baseline_doe_reference.idf # Official DOE Small Office Reference Model (ASHRAE 90.1)
│   ├── baseline_custom.idf        # Preserved baseline fallback model
│   └── weather.epw               # Chicago EPW weather dataset
├── src/
│   ├── ems_interface.py          # EMS sensors, actuators & ISO 7730 PMV engine
│   ├── carbon_signal.py          # Real EIA-930 grid carbon curve & 2H forecast
│   ├── llm_agent.py              # Predictive tool-calling agent with anomaly detection
│   ├── memory.py                 # Rolling self-correction decision history
│   ├── run_baseline.py           # Multi-zone baseline simulation runner
│   ├── run_ai_loop.py            # Autonomous closed-loop AI simulation runner
│   ├── mcp_server.py             # Model Context Protocol (MCP) Server wrapper
│   ├── telemetry_stream.py       # Hardware-agnostic real-time pub/sub gateway
│   └── config.py                 # Thermal comfort bounds, setpoints & startup validator
├── tests/
│   ├── test_bms.py               # Automated pytest unit test suite
│   └── test_data_lineage.py      # 26/26 data provenance & lineage verification tests
├── logs/
│   ├── baseline_output.csv       # Baseline simulation telemetry
│   ├── ai_output.csv             # AI closed-loop simulation telemetry
│   └── decisions_log.jsonl       # JSON-RPC LLM decision records & anomaly flags
├── dashboard/
│   └── app.py                    # Material Design 3 Streamlit BMS dashboard
├── docs/
│   ├── COMPLETE_SYSTEM_DOCUMENTATION.md # Master end-to-end frontend, backend & tools documentation
│   └── architecture.md           # Architecture documentation & evaluation mapping
├── test_full_pipeline.py         # Automated clean-state pipeline test harness
├── run_full_demo.py              # One-command live hackathon launcher
├── TESTING.md                    # Failure-mode & software quality testing documentation
├── DEMO_CHECKLIST.md             # Live hackathon presentation walkthrough guide
├── requirements.txt
└── README.md
```

---

## 🚀 Quickstart & Setup Guide

### 1. Prerequisites & Installation
Ensure Python 3.10+ is installed on your system.
```bash
# Clone the repository
git clone https://github.com/your-username/eco-loop-building-agents.git
cd eco-loop-building-agents

# Install dependencies
pip install -r requirements.txt
```

> **Note on LLM & Simulation Engines**:
> - **Zero-Setup Out-of-the-Box**: Out of the box, the system executes using its built-in advanced deep reasoning heuristic engine and pre-packaged EnergyPlus digital twin simulator — zero external API keys or Ollama installation required!
> - **Optional Ollama Local LLM**: If Ollama is running locally (`ollama run llama3.1` or `qwen2.5`), the system automatically detects the endpoint (`http://localhost:11434`) and transitions to live JSON-RPC tool calling.

---

### 2. One-Command Live Demo Launcher
Runs baseline simulation, AI control loop, and launches the interactive dashboard:
```bash
python run_full_demo.py
```
Open **`http://localhost:8501`** in your browser.

---

### 3. Clean-State Pipeline Verification Test Harness
To verify all simulations, data lineage, and dashboard compilation from a clean state:
```bash
python test_full_pipeline.py --force
```

---

### 4. Run Automated Test Suite
```bash
python tests/test_bms.py
python -m pytest tests/test_data_lineage.py
```


