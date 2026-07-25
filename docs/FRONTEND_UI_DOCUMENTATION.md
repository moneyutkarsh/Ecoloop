# 🎨 Eco-Loop Building Agents — Comprehensive Frontend UI & Design System Documentation

> **Document Scope**: Complete breakdown of the user interface architecture, design system tokens, typography, colors, layout components, interactive widgets, charts, and workspace specifications in [`dashboard/app.py`](file:///c:/Users/Utkarsh%20Dubey/.gemini/antigravity/Eco-Building%20Agent/dashboard/app.py).

---

## 🏛️ 1. Design System & Naming Architecture

The application uses a restrained modern SaaS Dark Theme built with Vanilla CSS variables, completely overriding default Streamlit theme elements.

### A. Unified Naming Protocol
- **Official Project Name**: `Eco-Loop Building Agents`
- **System / Agent Identifier**: `Eco-Loop BMS` / `Eco-Loop AI`
- All UI elements, header tags, chart tooltips, and documentation files strictly enforce 100% naming consistency.

---

### B. Color Palette Tokens (`:root`)
| Token Name | Hex / Value | Usage & Visual Role |
|---|---|---|
| `--bg-main` | `#080c14` | Deep obsidian main app canvas background. |
| `--bg-surface` | `#0f172a` | Slate surface background for header bars, tabs container, and section wrappers. |
| `--bg-card` | `#131c2e` | Flat surface card container background with 1px subtle border. |
| `--color-primary` | `#06b6d4` | Desaturated Professional Teal — Primary brand color for headers, borders, and main lines. |
| `--color-secondary` | `#94a3b8` | Cool gray text for subheadings, captions, and secondary labels. |
| `--color-success` | `#10b981` | Emerald Green — Comfort compliance and ISO 7730 band. |
| `--color-warning` | `#f59e0b` | Amber Gold — Playhead indicator rule and sensor fault anomaly callouts. |
| `--color-error` | `#ef4444` | Red — Unhandled exception alert states. |
| `--text-primary` | `#f8fafc` | Solid white text for titles, card values, and hero headings. |
| `--border-subtle` | `rgba(255, 255, 255, 0.08)` | Subtle 1px translucent card border. |

---

### C. Typography Architecture
- **Primary Sans-Serif**: `Inter` (Google Fonts, 2 weights: Regular `400` & Semi-Bold `600`) for all UI headings, body copy, tab titles, and button labels. No decorative text gradients.
- **Technical Monospace**: `JetBrains Mono` (Google Fonts, `400` & `600`) with `font-variant-numeric: tabular-nums` for numeric values, metric cards, timestamps, setpoints, and code payloads.

---

## 🎛️ 2. Main BMS Console Top Shell

The application opens directly into the main operating console without any intervening splash screens or marketing landing pages.

### Header Components:
1. **Header Navigation Bar**:
   - Title: `Eco-Loop Building Management System`.
   - Tagline: `Autonomous Building Energy & Carbon Optimization Engine • Enterprise BMS Platform`.
   - Single Status Indicator: `SYSTEM OPERATIONAL | 24 DECISIONS | 2 STRESS TESTS HANDLED`.
2. **Executive Summary Banner**:
   - Concise prose summary highlighting the ground truth results: "Eco-Loop AI reduced total HVAC energy consumption by **+9.9%** (8.28 kWh saved) and grid CO2 emissions by **+14.2%** (3.32 kg CO₂ offset) while maintaining **100.0%** thermal comfort compliance across a multi-zone 24-hour simulation."
3. **5 Metric Cards Row**:
   - **Card 1 (Hero Savings Metric)**: `HVAC Energy Saved vs Baseline` → `+9.9%`
   - **Card 2**: `TOTAL HVAC ENERGY` → `75.52 kWh` (Saved 8.28 kWh)
   - **Card 3**: `GRID CARBON OFFSETS` → `20.02 kg` (+14.2% Carbon Offset)
   - **Card 4**: `COMFORT COMPLIANCE` → `100.0%` (0 Violations)
   - **Card 5**: `STRESS EVENTS HANDLED` → `2 Events` (100% Zero-Crash Resilient)

---

## 📊 3. Workspace Breakdown

### Workspace 1: Performance & Live Playback Mode
- **Playback Controls**: Single `Play 24H Animation` / `Pause Replay` toggle button, `Live Real-Time Stream` checkbox, and timeline scrubber slider (`4` to `96`).
- **Chart 1: Fanger PMV Thermal Comfort Index**:
  - ISO 7730 green shaded comfort band `[-0.5, +0.5]`.
  - Baseline PMV curve (gray) vs Eco-Loop AI PMV curve (teal).
  - Amber vertical rule indicating active playhead step.
- **Chart 2: Cumulative HVAC Energy Consumption**:
  - Baseline cumulative energy (gray) vs Eco-Loop AI cumulative energy (teal).
  - Vertical dashed decision markers indicating 15-minute actuation cycles.

### Workspace 2: Deep Reasoning & Chain Inspector
- **Default State**: Defaults to **Step 36** (the sensor fault anomaly event) upon landing.
- **4-Step Reasoning Cards**: `1. ASSESS`, `2. FORECAST`, `3. TRADEOFF`, `4. DECIDE`.
- **Counterfactual Rationale Box**: Shows considered action vs rejected reason.
- **Stress Recovery Callout Panel**: Summarizes Step 36 (sensor fault) & Step 48 (malformed payload recovery).

### Workspace 3: Financial & Environmental ROI Impact Calculator
- Facility Floor Area slider (`500 m²` to `50,000 m²`) & Electricity Tariff Rate slider (`$0.08` to `$0.45 / kWh`).
- 4 Live Computed ROI metrics and 10-Year Cumulative Cash Savings projection chart.

### Workspace 4: MCP Agent Sandbox & Telemetry Stream
- Live interactive MCP tool call tester (`get_zone_state`, `set_thermostat_setpoint`, `get_carbon_intensity`, `set_lighting_level`).
- Hardware-Agnostic Ingestion Architecture diagram (BACnet / IoT Gateway ➔ Telemetry Stream Gateway ➔ MCP Server ➔ Eco-Loop LLM Agent ➔ EMS Actuators).
- Novelty Positioning comparison table (Model-Authoring Assistants vs Eco-Loop Autonomous Agent).
- Formatted 24-Hour Decision Feed dataframe, raw CSV downloads, Data Provenance SHA-256 panel, and Real-World EUI Validation benchmark table.
