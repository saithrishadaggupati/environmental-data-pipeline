# India AQI Data Pipeline

[

![Dashboard Preview](dashboard_preview.png)

](https://environmental-data-pipeline-2dnkog5rys5suebnkpqyzv.streamlit.app)

> Click the image to open the live dashboard

I got tired of reading air pollution headlines without seeing the actual numbers. So I built this — an automated pipeline that pulls live AQI data from 25 Indian cities every 6 hours, stores it in a cloud database, and visualizes it on an interactive map.

Delhi and Agra were consistently the most polluted. Kochi and Coimbatore stayed clean throughout. The south-north divide in air quality was sharper than I expected.

**[→ Live Streamlit Dashboard](https://environmental-data-pipeline-2dnkog5rys5suebnkpqyzv.streamlit.app)** · **[→ Live Dash Dashboard](https://environmental-data-pipeline.onrender.com)**

---

## What it does

Fetches live AQI data → cleans and validates it → loads into PostgreSQL → updates dashboards every 6 hours automatically. Includes a historical trend tracker, email alerts when cities hit dangerous levels, and an Excel export for reporting.

## Tech

Python · PostgreSQL · Neon · SQLAlchemy · Streamlit · Dash · Plotly · Folium · REST API · Pandas · Render

## Run it

```bash
git clone https://github.com/saithrishadaggupati/environmental-data-pipeline.git
pip install -r requirements.txt
cp .env.example .env
python -m src.scheduler
streamlit run dashboard/app.py

##Project Structure  

src/
├── ingestion/fetch_aqi.py         # API collection
├── transformation/clean_aqi.py    # Cleaning & labeling
├── transformation/data_quality.py # Quality checks
├── loading/load_to_postgres.py    # PostgreSQL + history
├── scheduler.py                   # Automation
├── export_excel.py                # Excel reports
├── alert.py                       # Email alerts
└── logger.py                      # Logging
sql/analysis_queries.py            # 7 SQL queries
dashboard/app.py                   # Streamlit dashboard
dashboard/dash_app.py              # Dash dashboard