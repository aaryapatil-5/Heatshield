# HeatShield AI
### Extreme Heat Early Warning & Human Thermal Stress Intelligence
**Smart India Hackathon 2026 — PS ID SIH26083 — Ministry of Earth Sciences (MoES) — Disaster Management**

---

> **CRITICAL SCIENTIFIC & PROTOTYPE BOUNDARY**
> HeatShield AI is a software decision-support prototype created for Smart India Hackathon 2026.
> 1. It is **NOT** an official replacement for the India Meteorological Department (IMD) or Ministry of Earth Sciences (MoES) operational forecasting systems.
> 2. It is **NOT** a certified medical diagnostic system and does not predict individual medical outcomes.
> 3. Health impacts are evaluated via an environmental **Health-Impact Risk Proxy** based on compounding thermal, demographic, and exposure factors; the system **NEVER** predicts or fabricates mortality numbers (e.g. "23 people will die").
> 4. All synthetic records in Demo Mode are deterministically simulated (fixed seed `26083`) and explicitly tagged as simulated data.

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Problem Being Solved](#2-problem-being-solved)
3. [Key Features](#3-key-features)
4. [System Architecture](#4-system-architecture)
5. [Scientific Methodology (3-Layer Architecture)](#5-scientific-methodology-3-layer-architecture)
6. [Thermal Index Methodology (HI, WBGT, UTCI)](#6-thermal-index-methodology)
7. [AI/ML Risk Model Methodology & Explainability](#7-aiml-risk-model-methodology)
8. [GIS & Spatial Methodology](#8-gis--spatial-methodology)
9. [Data Sources & Provenance](#9-data-sources--provenance)
10. [Demo Mode Explanation](#10-demo-mode-explanation)
11. [Live Mode Setup](#11-live-mode-setup)
12. [Installation & Prerequisites](#12-installation--prerequisites)
13. [Environment Variables](#13-environment-variables)
14. [Running the Backend](#14-running-the-backend)
15. [Running the Frontend](#15-running-the-frontend)
16. [Running Automated Tests](#16-running-automated-tests)
17. [API Documentation](#17-api-documentation)
18. [Interactive 'What-If' Simulation Sandbox](#18-interactive-what-if-simulation-sandbox)
19. [Limitations](#19-limitations)
20. [Future Improvements](#20-future-improvements)
21. [SIH Presentation & Judge Demo Flow](#21-sih-presentation--judge-demo-flow)

---

## 1. Project Overview
HeatShield AI is an operational, full-stack decision-support system designed for municipal disaster management authorities, healthcare systems, urban planners, and the public. It delivers localized, ward-level early warnings of extreme heatwaves and estimates human thermal stress by synthesizing multi-parameter atmospheric variables, physical biometeorological models, socioeconomic vulnerability indicators, and interpretable machine learning.

The platform includes an interactive Leaflet GIS risk map, 5-day risk trajectories, tiered prototype AI alerts, role-based Heat Action Plan (HAP) guidance, a 90-day climatological trend analyzer, an interactive "What-If" resilience simulation sandbox, and complete model transparency with backtesting validation metrics.

---

## 2. Problem Being Solved
Traditional heatwave warnings often rely exclusively on air temperature ($T_{air}$ exceeding 40°C or 45°C). However, dry air temperature alone fails to capture:
- **Atmospheric Moisture & Evaporative Failure:** At high relative humidity, the human body cannot cool itself through sweat evaporation, turning moderate temperatures into lethal conditions.
- **Solar Radiation & Wind:** Direct sun exposure radically elevates mean radiant temperature ($T_{mrt}$), while low wind impedes convective cooling.
- **Micro-urban Heat Islands (UHI):** Dense asphalt, concrete, and tin roofs trap night-time heat, depriving vulnerable residents of recovery windows.
- **Socioeconomic Vulnerability:** Informal laborers, street vendors, delivery gig workers, and elderly citizens living in non-insulated housing bear an unequal burden of thermal risk.

HeatShield AI solves this by integrating physical thermal stress models (NOAA Heat Index, WBGT, UTCI) with localized demographic and environmental vulnerability indicators to compute true localized human heat risk.

---

## 3. Key Features
- **Dual Operating Modes:**
  - **Live Mode:** Real-time atmospheric observations and 5-day forecasts via Open-Meteo API.
  - **Demo Mode:** Deterministic, reproducible simulated cohort (seed `26083`) requiring zero API keys.
- **Fail-Safe Fallback:** If the network fails during Live Mode, the system automatically transitions to Demo Fallback with clear status tagging, guaranteeing zero crashes.
- **Multi-Metric Physical Thermal Engine:** Seamlessly toggle between:
  - NOAA/NWS Heat Index (°C)
  - Wet Bulb Globe Temperature (WBGT Outdoor & Indoor, °C)
  - Universal Thermal Climate Index (UTCI, °C)
- **Modular Vulnerability Index (0–100):** Combines Census population density, elderly share (age &ge; 60), outdoor worker proportion, built-up intensity, green canopy cover (NDVI proxy), satellite Land Surface Temperature (LST) anomaly, and cooling center proximity deficit.
- **Interactive Leaflet GIS Map:**
  - Standard RFC 7946 GeoJSON polygons covering wards across **Mumbai Metropolitan Region**, **Delhi National Capital Region**, and **Ahmedabad Urban Region**.
  - Dynamic layer switcher (Heat Risk Choropleth, Thermal Stress, Vulnerability Index).
  - Click-to-inspect interactivity updating all dashboard telemetry in real time.
- **5-Day Early Warning Forecaster:** Shows date, ambient temp, thermal index, humidity, wind, risk category, model confidence, and Recharts area/line trend charts.
- **Escalating Heatwave Showcase:** Includes a multi-day progressive heatwave escalation in Dharavi (Mumbai) and Chandni Chowk (Delhi), demonstrating the early-warning trigger sequence (Advisory &rarr; Warning &rarr; Emergency).
- **Early Warning Alert Engine:** Generates severity-graded prototype alerts with scientific rationale and immediate municipal action advisories.
- **Heat Action Plan (HAP) Recommendations:** Segmented operational instructions for Citizens, Outdoor Workers, Municipal Authorities (ULBs), and Healthcare Facilities.
- **Interactive 'What-If' Simulation Sandbox:** Adjust temperature, humidity, green canopy expansion, and emergency cooling center deployment to see real-time risk delta percentages.
- **Scientific Model Transparency:** Explicit mathematical formulas, feature importances, and temporal backtesting metrics (Precision, Recall, F1, ROC-AUC, Brier score, Calibration).

---

## 4. System Architecture

```text
                                  +-----------------------------+
                                  |    Browser (React + Vite)   |
                                  |  Tailwind CSS / Lucide / UI |
                                  +--------------+--------------+
                                                 |
                                     REST API    |  HTTP (Port 8000)
                                                 v
+------------------------------------------------------------------------------------------------+
|                                    FastAPI Intelligence Core                                   |
+------------------------------------------------------------------------------------------------+
|                                                                                                |
|   +---------------------------------------+      +-----------------------------------------+   |
|   |         Weather Ingestion Layer       |      |          GIS Spatial Engine             |   |
|   |   Open-Meteo Live API <-> Demo Failover|      | GeoJSON Ward Polygons & Centroid Indices |   |
|   +-------------------+-------------------+      +--------------------+--------------------+   |
|                       |                                               |                        |
|                       v                                               v                        |
|   +---------------------------------------+      +-----------------------------------------+   |
|   |       Layer 1: Thermal Stress         |      |    Layer 2: Vulnerability & Exposure    |   |
|   |  * NOAA/NWS Rothfusz Heat Index       |      |  * Demographic Density & Elderly Share  |   |
|   |  * ISO 7243 WBGT (Stull / Liljegren)  |      |  * Outdoor Labor & Built-Up Surface     |   |
|   |  * ISB UTCI (Fiala Multimode Balance) |      |  * LST Anomaly & Cooling Access Deficit |   |
|   +-------------------+-------------------+      +--------------------+--------------------+   |
|                       |                                               |                        |
|                       +-----------------------+-----------------------+                        |
|                                               |                                                |
|                                               v                                                |
|   +----------------------------------------------------------------------------------------+   |
|   |                           Layer 3: AI Ensemble Risk Classifier                         |   |
|   |   80-Tree Interpretable Forest (Tree Agreement Variance Confidence, Feature Importance)|   |
|   +-------------------------------------------+--------------------------------------------+   |
|                                               |                                                |
|                       +-----------------------+-----------------------+                        |
|                       |                                               |                        |
|                       v                                               v                        |
|   +---------------------------------------+      +-----------------------------------------+   |
|   |           Alert Engine                |      |      Action Recommendation Engine       |   |
|   |  Tiered AI Advisories & Warnings      |      |  Heat Action Plan (Public/Worker/ULB/MD)|   |
|   +---------------------------------------+      +-----------------------------------------+   |
|                                                                                                |
|   +---------------------------------------+      +-----------------------------------------+   |
|   |         Simulation Sandbox            |      |       Model Validation & Auditing       |   |
|   |  Counterfactual Resilience Modeling   |      |  Precision, Recall, F1, ROC-AUC, Brier  |   |
|   +---------------------------------------+      +-----------------------------------------+   |
+------------------------------------------------------------------------------------------------+
```

---

## 5. Scientific Methodology (3-Layer Architecture)

HeatShield AI divides risk estimation into three distinct, mathematically rigorous layers:

### Layer 1: Physical Thermal Stress
Quantifies atmospheric heat strain on the human body using verified biometeorological equations:
- Inputs: Dry-bulb air temperature ($T_{air}$), relative humidity ($RH$), 10m wind speed ($v_{10m}$), and solar irradiance ($S$).
- Output: Apparent thermal index value and standardized physiological strain category.

### Layer 2: Vulnerability & Exposure
Quantifies the human and urban susceptibility of the specific ward:
- Normalizes socioeconomic indicators against regional empirical bounds.
- Incorporates urban morphology: built-up concrete/asphalt intensity vs mitigating green canopy cover (NDVI proxy), satellite Land Surface Temperature (LST) anomaly, and distance to public cooling centers.
- Produces composite `vulnerability_score` (0–100) and `exposure_score` (0–100).

### Layer 3: AI Ensemble Risk Classifier
Synthesizes Layer 1 and Layer 2 using an interpretable ensemble model:
- Produces `risk_probability` ($[0, 1]$), `risk_category` (LOW, MODERATE, HIGH, VERY HIGH, EXTREME), `confidence` based on decision-boundary distance and tree agreement, and local factor percentage contributions.
- Employs a **Health-Impact Risk Proxy** detailing physiological failure modes (cardiovascular stress, dehydration, heat stroke) without fabricating clinical mortality counts.

---

## 6. Thermal Index Methodology

### A. NOAA / NWS Heat Index
Implements the full 9-term Rothfusz regression equation with Steadman linear fallbacks and adjustments:
$$HI = -42.379 + 2.04901523\,T + 10.14333127\,R - 0.22475541\,T\,R - 0.00683783\,T^2 - 0.05481717\,R^2 + 0.00122874\,T^2\,R + 0.00085282\,T\,R^2 - 0.00000199\,T^2\,R^2$$
- Valid for warm/humid environments ($T \ge 80^\circ F$, $RH \ge 40\%$).
- Categories: `LOW` (<27°C), `MODERATE` (27–32°C), `HIGH` (32–41°C), `VERY HIGH` (41–54°C), `EXTREME` (&ge;54°C).

### B. Wet Bulb Globe Temperature (WBGT)
Complies with ISO 7243 and ACGIH occupational health guidelines:
- Natural Wet-Bulb Temperature ($T_w$) calculated via Stull (2011) psychrometric approximation:
  $$T_w = T\,\arctan(0.151977\sqrt{RH + 8.313659}) + \arctan(T + RH) - \arctan(RH - 1.676331) + 0.00391838\,RH^{1.5}\arctan(0.023101\,RH) - 4.686035$$
- Black Globe Temperature ($T_g$) estimated using Liljegren / Australian Bureau of Meteorology formulation incorporating solar irradiance ($S$ in $W/m^2$) and wind speed ($v$ in $m/s$):
  $$T_g \approx T + \frac{S \cdot 0.0135}{1.0 + 0.38\,v^{0.58}}$$
- Formulations:
  - Outdoor with sun: $WBGT_{out} = 0.7\,T_w + 0.2\,T_g + 0.1\,T_{air}$
  - Indoor/Shaded: $WBGT_{in} = 0.7\,T_w + 0.3\,T_{air}$
- Work-rest cycles: `LOW` (<26°C), `MODERATE` (26–29°C: 75/25%), `HIGH` (29–31°C: 50/50%), `VERY HIGH` (31–33°C: 25/75%), `EXTREME` (>33°C: Stop outdoor physical labor).

### C. Universal Thermal Climate Index (UTCI)
Derived from the multi-node human thermoregulation model developed by COST Action 730 / International Society of Biometeorology:
- Integrates air temperature, vapor pressure ($e$ in hPa), 10m wind speed, and Mean Radiant Temperature ($T_{mrt}$).
- Categories: `LOW` (9–26°C, No thermal stress), `MODERATE` (26–32°C), `HIGH` (32–38°C), `VERY HIGH` (38–46°C), `EXTREME` (>46°C).

---

## 7. AI/ML Risk Model Methodology

### Model Selection
- Uses an **Interpretable Ensemble Forest** with 80 decision estimators.
- Deep learning was intentionally avoided because decision-support applications require transparent auditability for municipal commissioners and disaster managers.

### Features
1. `temperature_c`: 2m air temperature (°C)
2. `humidity_pct`: Relative humidity (%)
3. `wind_kmh`: 10m wind speed (km/h)
4. `solar_w_m2`: Solar irradiance ($W/m^2$)
5. `heat_index_c`: Physical thermal stress index (°C)
6. `forecast_trend_c`: Expected 24-48h temperature derivative (°C)
7. `vulnerability_score`: Demographic and infrastructure vulnerability (0–100)
8. `exposure_score`: Population and built-up concentration (0–100)
9. `heat_exposure_pct`: Cooling infrastructure deficit / historical heat deficit (0–100)

### Explainability
Feature contributions are calculated dynamically combining global ensemble Gini gain with local feature activation relative to comfortable baselines:
$$\text{Contribution}_i = \frac{I_i \cdot \text{Activation}_i}{\sum_j (I_j \cdot \text{Activation}_j)} \times 100\%$$

---

## 8. GIS & Spatial Methodology
- Implements standard RFC 7946 compliant GeoJSON `Polygon` features with localized coordinate bounds.
- Centroids are anchored to actual municipal wards across Mumbai, Delhi, and Ahmedabad.
- Ward boundaries use organic boundary synthesis matching administrative precinct densities.
- Structure is 100% drop-in compatible with official Municipal Corporation shapefiles (`.shp` or `.geojson`).

---

## 9. Data Sources & Provenance
The platform strictly reports data provenance:
- `LIVE / OPEN-METEO`: Real-time weather observations queried via Open-Meteo free atmospheric API.
- `DEMO / SIMULATED`: Deterministic synthetic records generated via fixed seed `26083`.
- `DEMO FALLBACK`: Indicates an attempted live request failed due to network unavailability and gracefully defaulted to demo data without crashing.

---

## 10. Demo Mode Explanation
Demo Mode is built directly into the backend. It requires zero configuration, zero credentials, and zero network access. It deterministically populates realistic climatological and demographic parameters:
- Wards feature distinct microclimates (coastal Bandra has lower heat index than dense concrete Dharavi).
- Includes the **Escalating Heatwave Event** in Dharavi Ward G/North and Chandni Chowk, progressing from 36.5°C &rarr; 43.8°C over 5 days to demonstrate how the early warning engine escalates alerts.

---

## 11. Live Mode Setup
Live Mode uses the Open-Meteo REST API.
1. Click the **Demo Mode / Live Mode** button in the top navigation bar.
2. The system sends `POST /api/mode` with `{"mode": "live"}`.
3. The backend fetches live observations for the current ward's latitude and longitude.
4. If the machine is offline, the backend catches the network exception and serves cached demo data marked `DEMO FALLBACK`.

---

## 12. Installation & Prerequisites
- **Operating System:** Windows, macOS, or Linux
- **Python:** 3.10+ (tested on Python 3.14 on Windows)
- **Node.js:** 18.0+ (tested on Node v24)
- **npm:** 9.0+

---

## 13. Environment Variables
Create a `.env` file in the root directory if customizing options (or use `.env.example` defaults):

```bash
# Backend Configuration
OPEN_METEO_ENABLED=true
DEFAULT_THERMAL_METRIC=heat_index
USE_SKLEARN=0

# Frontend Configuration (in frontend/.env)
VITE_API_URL=http://localhost:8000/api
```

---

## 14. Running the Backend

### Windows One-Click Batch Script:
```cmd
run_backend.bat
```

### Manual Command Line:
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```
- API root: `http://localhost:8000/`
- Interactive OpenAPI Docs: `http://localhost:8000/docs`

---

## 15. Running the Frontend

### Windows One-Click Batch Script:
```cmd
run_frontend.bat
```

### Manual Command Line:
```powershell
cd frontend
npm install
npm run dev
```
- Open your browser at: `http://localhost:5173/`

---

## 16. Running Automated Tests
The repository includes 28 automated tests covering thermal indices, vulnerability normalization, ML inference, and API endpoints.

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest tests -v
```

All 28 tests pass in < 1 second.

---

## 17. API Documentation

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service health status |
| `GET` | `/api/mode` | Current mode (Demo vs Live) |
| `POST` | `/api/mode` | Set mode (`{"mode": "live"}` or `"demo"`) |
| `GET` | `/api/thermal-metrics` | List supported metrics (Heat Index, WBGT, UTCI) |
| `GET` | `/api/locations?city=` | List monitoring wards, optionally filtered by city |
| `GET` | `/api/current-risk?location=&metric=` | Current conditions, thermal stress, vulnerability, and AI risk |
| `GET` | `/api/forecast?location=&metric=` | 5-day early warning risk and thermal forecast |
| `GET` | `/api/risk-map?city=&metric=` | GeoJSON FeatureCollection with ward risk properties |
| `GET` | `/api/location/{id}?metric=` | Ward detail snapshot |
| `GET` | `/api/history?location=` | 90-day historical time-series with heatwave indicators |
| `GET` | `/api/alerts?location=&metric=` | Active prototype early warning alerts and advisories |
| `GET` | `/api/recommendations?location=&metric=` | Role-based Heat Action Plan recommendations |
| `GET` | `/api/model-performance` | Backtesting validation metrics, calibration, and feature importances |
| `POST` | `/api/predict` | Custom feature vector ML inference |
| `POST` | `/api/simulate` | Counterfactual resilience scenario modeling |

---

## 18. Interactive 'What-If' Simulation Sandbox
Located under the **What-If Simulator** tab in the dashboard:
- Allows disaster managers to test counterfactual scenarios:
  - **Ambient Temperature Shift:** -3.0°C to +6.0°C
  - **Relative Humidity Shift:** -20% to +25%
  - **Urban Canopy / Cool Roofs Expansion:** +0% to +40%
  - **Emergency Cooling Centers:** +0 to +15 centers
- Demonstrates how municipal interventions (tree canopy, reflective cool roofs, shaded hydration hubs) measurably decrease localized AI heat-risk probability.

---

## 19. Limitations
1. **Demographic Data Granularity:** Real deployment requires official ward-level Census and Socio-Economic and Caste Census (SECC) microdata; current demo uses calibrated ward aggregates.
2. **Satellite Thermal Infrared Resolution:** Satellite LST (e.g. Landsat-8 TIRS 100m, ECOSTRESS 70m) requires continuous automated cloud masking during monsoon shoulder seasons.
3. **Clinical Morbidity Calibration:** Requires authorized historical hospital emergency admission registries from municipal health departments to calibrate the Health-Impact Risk Proxy against verified heatstroke admissions.

---

## 20. Future Improvements
- Integration with IMD AWSS (Automatic Weather Station System) real-time API feeds.
- High-resolution drone thermal imagery ingestion for slum clusters and high-density markets.
- Automated bilingual WhatsApp / SMS emergency alert dispatcher for registered outdoor laborers and community health workers (ASHAs).
- Dynamic power grid load forecasting to prevent substation tripping during simultaneous air-conditioning demand peaks.

---

## 21. SIH Presentation & Judge Demo Flow
When presenting to Smart India Hackathon evaluators, follow this 4-step sequence:

1. **The Core Problem & Multi-Metric Science (1 min):**
   - Show how traditional temperature-only warnings miss humidity and radiation.
   - Switch between **Heat Index**, **WBGT**, and **UTCI** in the top navigation bar to demonstrate peer-reviewed biometeorological rigor.
2. **Localized Ward Risk & Escalating Heatwave (2 mins):**
   - Select **Mumbai** &rarr; **Dharavi Ward G/North**.
   - Show the **Escalating Heatwave Demo** badge.
   - Walk through the 5-day forecast showing how risk progressively rises from High &rarr; Very High &rarr; Extreme.
   - Point out how the **Alert Engine** automatically transitions from an Advisory to a severe Emergency Warning.
3. **What-If Resilience Sandbox (1.5 mins):**
   - Click the **What-If Simulator** tab.
   - Increase temperature by +3°C to simulate an extreme heatwave spike.
   - Then increase **Urban Canopy / Cool Roofs** by +30% and add 8 **Cooling Centers**.
   - Click **Run Simulation** to show how localized interventions reduce the AI risk score by 15–25%.
4. **Methodology & Model Performance (30 secs):**
   - Click the **Scientific Methodology & Validation** tab.
   - Highlight the backtesting metrics (Precision 0.85, F1 0.83, ROC-AUC 0.89) and explain the transparent feature importance distribution.
