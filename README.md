# India AQI Data Pipeline

[

![Live Dashboard](https://img.shields.io/badge/Live%20Dashboard-Click%20Here-brightgreen)

](https://environmental-data-pipeline-2dnkog5rys5suebnkpqyzv.streamlit.app)



![Dashboard Preview](dashboard_preview.png)



---

I got tired of reading air pollution headlines without seeing the actual numbers. So I built this — an automated pipeline that pulls live AQI data from 25 Indian cities every 6 hours, stores it in a cloud database, and visualizes it on an interactive map.

Delhi and Agra were consistently the most polluted. Kochi and Coimbatore stayed clean throughout. The south-north divide in air quality was sharper than I expected.

**[Live Streamlit Dashboard](https://environmental-data-pipeline-2dnkog5rys5suebnkpqyzv.streamlit.app)** · **[Live Dash Dashboard](https://environmental-data-pipeline.onrender.com)**

---

## What I found

- Delhi and Agra rank highest for pollution across all readings
- Kochi and Coimbatore consistently stay in the "Good" range
- Tier-3 cities like Patna and Varanasi exceed safe PM2.5 limits more often than metros
- Clear south-north divide — southern cities average 40% lower AQI than northern ones

---

## How it works

Open-Meteo API -> Python ETL -> PostgreSQL (Neon) -> Streamlit + Dash

**Pipeline:**
- `fetch_aqi.py` — pulls live AQI for 25 cities every 6 hours
- `clean_aqi.py` — validates and labels air quality
- `load_to_postgres.py` — upserts into Neon cloud PostgreSQL
- `scheduler.py` — automates the pipeline
- `alert.py` — email alerts when cities hit dangerous levels
- `export_excel.py` — Excel export for reporting

**SQL Analysis (7 queries):**
- Top polluted cities
- Average AQI by category
- Cities above danger threshold
- Clean vs polluted ratio (window function)
- City rankings vs national average (RANK + window function)
- High risk city CTE analysis
- City-tier comparison — Metro vs Tier-2 vs Tier-3

**Dashboards:**
- Interactive India map with AQI bubbles
- Historical trend tracker
- Both Power BI and Tableau versions included

---

## Tech

Python · Pandas · PostgreSQL · Neon · SQLAlchemy · Streamlit · Dash · Plotly · Folium · Power BI · Tableau · Render

---

## Run it

```bash
git clone https://github.com/saithrishadaggupati/environmental-data-pipeline.git
pip install -r requirements.txt
cp .env.example .env
python -m src.scheduler
streamlit run dashboard/app.py
## Project Structure

src/
- ingestion/fetch_aqi.py         # API collection
- transformation/clean_aqi.py    # Cleaning & labeling
- transformation/data_quality.py # Quality checks
- loading/load_to_postgres.py    # PostgreSQL + history
- scheduler.py                   # Automation
- export_excel.py                # Excel reports
- alert.py                       # Email alerts
- logger.py                      # Logging

sql/analysis_queries.py          # 7 SQL queries
dashboard/app.py                 # Streamlit dashboard
dashboard/dash_app.py            # Dash dashboard