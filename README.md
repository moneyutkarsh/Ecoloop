# ⚡ EcoLoop AI — Autonomous Building Intelligence OS

> **Flagship Autonomous Building Energy & Carbon Optimization Platform**  
> An autonomous, predictive Building Management System (BMS) that pairs the official **U.S. Department of Energy (DOE) Commercial Reference Building** model (`RefBldgSmallOfficeNew2004_Chicago.idf` via pyenergyplus EMS API) with an open-source Large Language Model (**Ollama / Llama 3.1 / Qwen 2.5**) and the **Model Context Protocol (MCP)**, rendered in a Siemens/Palantir-grade Enterprise Control Center UI.

---

## 🌟 Key Performance Benchmarks & Results

| Metric | Unmodified DOE Baseline | EcoLoop AI Autonomous | Improvement / Benchmark |
| :--- | :---: | :---: | :---: |
| **Total HVAC Energy** | `83.80 kWh` | **`75.52 kWh`** | **`+9.9% Energy Savings`** |
| **Grid Carbon Footprint** | `23.35 kg CO2` | **`20.02 kg CO2`** | **`+14.2% CO2 Offsets`** |
| **Thermal Comfort (PMV)** | `0 Violations` | **`0 Violations`** | **`100.0% ISO 7730 Compliance`** |
| **Annualized Cost Savings** | `$0` | **`$10,883 / yr`** | **Scaled to 5,000 m² office** |
| **Stress & Fault Resilience** | `N/A` | **`2 Fault Events`** | **`100% Zero-Crash Resilient`** |

---

## 🖥️ Flagship Enterprise UI & Digital Twin Redesign

EcoLoop AI features a commercial-grade **AI Control Center** designed for high-stakes operational environments:

### Key UI Features
* **Glassmorphism Dark Theme**: Built on a `#050816 → #111827` multi-stop gradient background with custom glass panel cards (`backdrop-filter: blur(20px)`), vibrant glows, and responsive typography (Outfit + Inter + JetBrains Mono).
* **8 Hero KPI Cards**: Real-time animated hero metrics featuring Energy Saved (`+9.9%`), Carbon Reduced (`14.2%`), Comfort Score (`100%`), Annual ROI (`$10.8k`), Peak Occupancy (`10`), Outdoor Weather (`26.1°C`), AI Confidence (`98%`), and Building Health (`99%`).
* **Live 3-Column Control Center**:
  * 👈 **Left Panel**: SVG Floor Plan color-coded by real-time PMV, Occupancy Heatmap bar series, Grid Carbon Intensity widget (`LOW`/`MED`/`HIGH`), and automated Fault Detection alert badges.
  * 🎯 **Center Panel**: **Animated SVG Digital Twin** featuring rotating HVAC fan blades (AHU-01 & AHU-02), live room temperature overlays, animated airflow trails, an Energy Flow chain (`Grid ➔ Battery ➔ Building ➔ HVAC ➔ Zones`), and concentric Building Health SVG progress rings.
  * 👉 **Right Panel**: **AI Brain Panel** displaying step-by-step streaming LLM reasoning logs, live Agent Subsystem health badges (Planner, Reasoner, Memory, Predictor), scrolling MCP Tool Call log, and Weather widget.
* **Bottom Control Section**: Visual AI Decision Timeline with connected node markers, Energy Savings Counter (`8.28 kWh` today), PMV Comfort sparklines, and cumulative Energy/Carbon area charts.
* **Floating Toast Notifications**: Top-right slide-in alerts announcing live AI setpoint executions.

---

## 🏛️ System Architecture & Standards

- **DOE Reference Model**: Based on PNNL/NREL CBECS survey data for a Small Commercial Office (511 m² / 5,500 ft²) under **ASHRAE Standard 90.1-2004**.
- **ISO 7730 Fanger PMV Engine**: Computes Predicted Mean Vote (PMV) thermal comfort in real time based on dry-bulb temperature, mean radiant temperature, relative humidity, air velocity, metabolic rate, and clothing insulation. Comfort standard enforced strictly between `[-0.5, +0.5]`.
- **Model Context Protocol (MCP)**: Implements standard JSON-RPC 2.0 tool execution (`get_zone_state`, `get_carbon_intensity`, `set_thermostat_setpoint`, `set_lighting_level`).
- **Zero-Crash Fault Resilience**: Built-in anomaly detection and defensive fallback mechanisms safely handle telemetry sensor drift and malformed LLM tool call payloads with zero downtime.

---

## 📑 Interactive Dashboard Workspaces

The platform includes 5 modular workspace environments:

1. 🎛️ **Live Control Center**: The main Palantir-style AI control center with Digital Twin, AI Brain, and 3-column operational layout.
2. 📊 **Performance & Live Playback**: 24-hour interactive simulation replay toolbar with playhead scrubber and dual Altair comfort/energy timelines.
3. 🧠 **Deep Reasoning Inspector**: Step-by-step breakdown of the agent's 4-stage internal reasoning chain (**ASSESS ➔ FORECAST ➔ TRADEOFF ➔ DECIDE**) alongside counterfactual trade-off analysis and stress recovery logs.
4. 💰 **Financial & Environmental ROI Calculator**: Interactive scaling tool projecting annual energy cost savings and 10-year cumulative ROI across custom building square footage (`m²`) and electricity rates (`$/kWh`).
5. 🧪 **MCP Sandbox & Telemetry Stream**: Interactive tool-calling simulator for testing custom telemetry payloads, multi-zone topology inspection, and raw CSV telemetry downloads.

---

## 📁 Project Layout

```
eco-loop-building-agents/
├── EXECUTIVE_SUMMARY.md          # One-page 60-second executive summary
├── README.md                     # Master project documentation
├── requirements.txt              # Python dependency manifest
├── run_full_demo.py              # One-command live hackathon launcher
├── test_full_pipeline.py         # Automated clean-state pipeline test harness
├── TESTING.md                    # Failure-mode & software quality testing documentation
├── DEMO_CHECKLIST.md             # Hackathon presentation walkthrough guide
│
├── dashboard/
│   └── app.py                    # EcoLoop AI Flagship Control Center UI (Streamlit)
│
├── src/
│   ├── ems_interface.py          # EMS sensors, actuators & ISO 7730 PMV engine
│   ├── carbon_signal.py          # Real EIA-930 grid carbon curve & 2-hour forecast
│   ├── llm_agent.py              # Predictive tool-calling agent & anomaly detection
│   ├── memory.py                 # Rolling self-correction decision memory
│   ├── run_baseline.py           # Multi-zone baseline simulation runner
│   ├── run_ai_loop.py            # Autonomous closed-loop AI simulation runner
│   ├── mcp_server.py             # Model Context Protocol (MCP) Server wrapper
│   ├── telemetry_stream.py       # Real-time pub/sub telemetry streaming gateway
│   └── config.py                 # Comfort bounds, setpoints & startup validator
│
├── models/
│   ├── baseline_doe_reference.idf # Official DOE Small Office Reference Model (ASHRAE 90.1)
│   ├── baseline_custom.idf        # Preserved baseline fallback model
│   └── weather.epw               # Chicago EPW weather dataset
│
├── tests/
│   ├── test_bms.py               # Pytest unit test suite
│   └── test_data_lineage.py      # Data provenance & lineage verification tests
│
├── logs/
│   ├── baseline_output.csv       # Baseline simulation telemetry
│   ├── ai_output.csv             # AI closed-loop simulation telemetry
│   └── decisions_log.jsonl       # JSON-RPC LLM decision records & anomaly flags
│
└── docs/
    ├── COMPLETE_SYSTEM_DOCUMENTATION.md # Master end-to-end documentation
    ├── FRONTEND_UI_DOCUMENTATION.md     # UI design system & architecture docs
    └── architecture.md                  # System architecture & evaluation mapping
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

### 3. Direct Dashboard Launch
If simulation logs are already generated:
```bash
python -m streamlit run dashboard/app.py
```

---

### 4. Automated Testing & Data Lineage Verification
```bash
# Run automated unit test suite
python tests/test_bms.py

# Run data lineage and integrity verification
python -m pytest tests/test_data_lineage.py

# Run full pipeline clean-state verification harness
python test_full_pipeline.py --force
```

---

## 📄 Executive Summary & Full Documentation

- 📋 **Executive Summary**: [`EXECUTIVE_SUMMARY.md`](EXECUTIVE_SUMMARY.md)
- 🎨 **Frontend UI Documentation**: [`docs/FRONTEND_UI_DOCUMENTATION.md`](docs/FRONTEND_UI_DOCUMENTATION.md)
- 📖 **Complete System Documentation**: [`docs/COMPLETE_SYSTEM_DOCUMENTATION.md`](docs/COMPLETE_SYSTEM_DOCUMENTATION.md)
- 🏗️ **Architecture & Evaluation Mapping**: [`docs/architecture.md`](docs/architecture.md)
- 🧪 **Testing & Quality Assurance**: [`TESTING.md`](TESTING.md)
- 🎙️ **Demo Presentation Walkthrough**: [`DEMO_CHECKLIST.md`](DEMO_CHECKLIST.md)

---

<p align="center">
  <b>EcoLoop AI Platform</b> • Powered by EnergyPlus, Model Context Protocol (MCP) & LLM Intelligence
</p>
