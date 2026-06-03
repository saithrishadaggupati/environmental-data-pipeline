\# Data Dictionary — Environmental Air Quality Pipeline



\## Table: aqi\_readings



| Column | Type | Description | Example |

|--------|------|-------------|---------|

| city | string | Name of Indian city | Delhi |

| aqi\_index | integer | European AQI score (0-500) | 142 |

| pm2\_5 | float | Fine particulate matter (µg/m³) | 45.3 |

| pm10 | float | Coarse particulate matter (µg/m³) | 78.1 |

| co | float | Carbon monoxide level (µg/m³) | 201.4 |

| air\_quality\_label | string | Risk classification | Unhealthy |

| timestamp | datetime | Data collection time | 2026-06-03 06:00:00 |



\## AQI Classification Rules



| AQI Range | Label | Health Impact |

|-----------|-------|---------------|

| 0 - 50 | Good | No health risk |

| 51 - 100 | Moderate | Acceptable quality |

| 101 - 200 | Unhealthy | Health effects possible |

| 200+ | Hazardous | Serious health effects |



\## Data Source

\- API: Open-Meteo Air Quality API

\- Coverage: 100+ Indian cities

\- Refresh Rate: Daily (automated via GitHub Actions)

\- Owner: Sai Thrisha Daggupati

