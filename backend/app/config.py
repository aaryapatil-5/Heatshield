from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / 'data'
DEMO_SEED = 26083

# Configurable Risk Classification Thresholds
# Model probability < threshold maps to the category
RISK_THRESHOLDS = {
    'LOW': 0.20,
    'MODERATE': 0.45,
    'HIGH': 0.68,
    'VERY HIGH': 0.84,
    'EXTREME': 1.01,
}

# Heatwave Risk Colors for GIS Map and UI
RISK_COLORS = {
    'LOW': '#10b981',       # Emerald Green
    'MODERATE': '#f59e0b',  # Amber Yellow
    'HIGH': '#f97316',      # Orange
    'VERY HIGH': '#ef4444', # Bright Red
    'EXTREME': '#991b1b'    # Deep Maroon / Crimson
}

# Modular Vulnerability Index Weights (Sum to 1.0)
# Designed for transparent urban heat resilience prioritization
VULNERABILITY_WEIGHTS = {
    'pop_density': 0.20,             # People / sq.km exposure pressure
    'elderly_pct': 0.15,             # Demographic susceptibility (age >= 60)
    'outdoor_worker_pct': 0.20,      # Physical occupational exposure
    'built_up_pct': 0.15,            # Impervious surface & urban heat island trap
    'green_cover_inverse': 0.10,     # Lack of mitigating canopy/water bodies
    'lst_anomaly': 0.10,             # Land Surface Temperature satellite anomaly
    'cooling_access_deficit': 0.10   # Lack of proximity to cooling shelters/water points
}

# Modular Exposure Index Weights (Sum to 1.0)
EXPOSURE_WEIGHTS = {
    'pop_density': 0.60,
    'built_up_pct': 0.40
}

# Normalization Upper Bounds for Demographic & Environmental Indicators
NORMALIZATION_BOUNDS = {
    'pop_density_max': 50000.0,      # People / sq.km (dense Indian urban wards)
    'elderly_pct_max': 25.0,         # % of ward population
    'outdoor_worker_max': 50.0,      # % of working population in outdoor conditions
    'lst_anomaly_max': 6.0,          # °C thermal anomaly above regional baseline
    'cooling_deficit_max': 100.0     # 0 = high access, 100 = severe cooling desert
}

# Weather API Configuration
OPEN_METEO_BASE = 'https://api.open-meteo.com/v1/forecast'
OPEN_METEO_ENABLED = os.getenv('OPEN_METEO_ENABLED', 'true').lower() == 'true'
DEFAULT_THERMAL_METRIC = os.getenv('DEFAULT_THERMAL_METRIC', 'heat_index')
