# India AQI Data Pipeline

[
![Live Dashboard](https://img.shields.io/badge/Live%20Dashboard-Click%20Here-brightgreen)
](https://environmental-data-pipeline-2dnkog5rys5suebnkpqyzv.streamlit.app)



![Dashboard Preview](dashboard_preview.png)



---

I wanted to understand how air quality varies across India beyond just the major metros. So I built an end-to-end data pipeline that tracks AQI data from 101 Indian cities, stores it in MongoDB, and visualizes trends through interactive dashboards.

The system automatically collects, processes, and analyzes air quality data, making it easy to compare pollution levels across regions and identify patterns over time. Building this gave me hands-on experience with data engineering, cloud databases, pipeline automation, and visualization — all on real environmental data.

**[Live Streamlit Dashboard](https://environmental-data-pipeline-2dnkog5rys5suebnkpqyzv.streamlit.app)** · **[Live Dash Dashboard](https://environmental-data-pipeline.onrender.com)**

---

## What the data shows

- Delhi and Agra consistently rank as the most polluted cities across all runs
- Kochi, Coimbatore, and Thiruvananthapuram hold steady in the "Good" range
- Tier-3 cities like Patna and Varanasi exceed safe PM2.5 limits more often than metros
- A clear south-north divide — southern cities average 40% lower AQI than northern ones

| Region | Cities | Avg AQI | Category |
|--------|--------|---------|----------|
| North | Delhi, Agra, Patna | ~150 | Unhealthy |
| South | Kochi, Coimbatore, Chennai | ~35 | Good |

---

## How it works

Open-Meteo API → Python ETL → MongoDB Atlas (raw) → CSV → Streamlit + Dash

**Pipeline components:**
- fetch_aqi.py — pulls live AQI for 101 cities with retry logic (3 attempts per city)
- clean_aqi.py — validates data and assigns air quality labels
- mongo_store.py — stores raw readings in MongoDB Atlas
- scheduler.py — automates the full pipeline every 6 hours
- alert.py — sends email alerts when cities hit dangerous AQI levels
- export_excel.py — Excel export for offline reporting

**PostgreSQL Analysis (8 queries, running on Neon cloud):**
- Top polluted cities
- Average AQI by category
- Cities above danger threshold (AQI > 200)
- Clean vs polluted city ratio
- City rankings vs national average (window function)
- High risk city CTE analysis
- City-tier comparison — Metro vs Tier-2 vs Tier-3
- Time-of-day AQI pattern analysis

**Statistical analysis:**
- Descriptive stats — mean, median, std dev, skewness (2.56), kurtosis (6.99)
- Outlier detection via Z-score — Delhi and Agra flagged as statistical outliers
- AQI distribution by category across all 101 cities
- Hypothesis test — Mann-Whitney U test (non-parametric) comparing North vs South India AQI — p-value 0.009, statistically significant

**Data quality:** 4 automated checks on every pipeline run — null check, range check, duplicate check, freshness check

**Schema validation:** Pydantic models enforce field types and constraints on every AQI record before storage — city name, AQI range (0–500), and timestamp are all validated with structured error reporting

**Tests:** 9 pytest tests covering label boundaries and city data validation

**Dashboards:**
- Interactive India map with AQI bubbles for all 101 cities
- Bar chart, pie chart, scatter plot, and trend tracker
- Both Streamlit and Dash versions live

---

## Tech stack

Python · Pandas · PostgreSQL (Neon) · MongoDB Atlas · PyMongo · Streamlit · Dash · Plotly · Folium · Docker · GitHub Actions · Render
---

## Run locally

git clone https://github.com/saithrishadaggupati/environmental-data-pipeline.git
cd environmental-data-pipeline
pip install -r requirements.txt
cp .env.example .env
python -m src.ingestion.fetch_aqi
python -m src.loading.mongo_store
streamlit run dashboard/app.py

## Run with Docker

docker-compose up

## Run tests

pytest tests/ -v
