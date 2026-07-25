# ⚡ Eco-Loop Building Agents — One-Page Executive Summary

> **Autonomous Building Energy & Carbon Optimization Engine**  
> **Project**: Autonomous, Predictive Smart Building Energy & Carbon Optimization Engine  
> **Repository**: [Eco-Loop Building Agents](file:///c:/Users/Utkarsh%20Dubey/.gemini/antigravity/Eco-Building%20Agent)

---

## 🎯 The One-Sentence Pitch
**Eco-Loop Building Agents** is an autonomous, predictive Building Management System (BMS) that pairs physics-based **EnergyPlus** multi-zone thermal simulation with open-source Large Language Models (**Ollama / Llama 3.1 / Qwen 2.5**) via the **Model Context Protocol (MCP)** to continuously optimize HVAC energy draw and grid carbon emissions in real time with zero human in the loop.

---

## 📊 4 Headline Performance Benchmarks

```
┌─────────────────────────┬─────────────────────────┬─────────────────────────┬─────────────────────────┐
│  ⚡ HVAC ENERGY SAVED   │  🌱 GRID CARBON OFFSET   │  ✅ COMFORT COMPLIANCE  │   🛡️ ZERO-CRASH SAFETY  │
│         +9.9%           │         +14.2%          │         100.0%          │       100% PASS         │
│  (8.28 kWh Saved/Day)   │   (3.32 kg CO2 Offset)  │  (ISO 7730 PMV Standard)│ (2 Stress Events Handled)│
└─────────────────────────┴─────────────────────────┴─────────────────────────┴─────────────────────────┘
```

| Performance Metric | Unmodified DOE Baseline | Eco-Loop AI Autonomous | Improvement / Status |
|---|:---:|:---:|:---:|
| **Total HVAC Energy** | `83.80 kWh` | **`75.52 kWh`** | **`+9.9% Energy Saved`** |
| **Grid Carbon Footprint** | `23.35 kg CO2` | **`20.02 kg CO2`** | **`+14.2% CO2 Offset`** |
| **PMV Comfort Violations** | `0` | **`0`** | **`100.0% ISO 7730 Compliant`** |
| **Operational Stress Resilience** | `0` | **`2 Fault Events`** | **`100% Zero-Crash Resilient`** |

---

## 🏛️ Key Technical Differentiation & Rigor

- **Official DOE Reference Model**: Built on the PNNL/NREL Commercial Reference Building Model (`RefBldgSmallOfficeNew2004_Chicago.idf`, 511 m² / 5,500 ft² Small Office under ASHRAE 90.1-2004).
- **Real Grid Carbon Signal**: Ingests real historical EIA-930 / PJM ComEd grid emissions data for Chicago, IL (July 1, 2024) with 15-minute sub-hourly linear interpolation.
- **Production MCP Server Protocol**: Full Model Context Protocol JSON-RPC server implementation (`src/mcp_server.py`) exposing standardized tool calls (`get_zone_state`, `set_thermostat_setpoint`).
- **Real-World EUI Validation**: Annualized full-building HVAC EUI of **53.9 kWh/m²/year** validated directly against published U.S. DOE CBECS commercial building benchmarks (**50.0 – 90.0 kWh/m²/year**).
- **Closed-Loop Live Operation**: Unlike research assistants that help humans *author* models, Eco-Loop operates a live model continuously in closed-loop control.

---

## 🚀 Quickstart & Complete Technical Documentation

1. **Launch Interactive Console**:
   ```bash
   python run_full_demo.py
   ```
2. **Run Pipeline Verification Test Harness**:
   ```bash
   python test_full_pipeline.py --force
   ```
3. **Deep Architecture & Evaluation Document**: [`docs/architecture.md`](file:///c:/Users/Utkarsh%20Dubey/.gemini/antigravity/Eco-Building%20Agent/docs/architecture.md)
4. **Master End-to-End System Documentation**: [`docs/COMPLETE_SYSTEM_DOCUMENTATION.md`](file:///c:/Users/Utkarsh%20Dubey/.gemini/antigravity/Eco-Building%20Agent/docs/COMPLETE_SYSTEM_DOCUMENTATION.md)
