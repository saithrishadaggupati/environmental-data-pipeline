# India AQI Data Pipeline

I kept reading headlines about air pollution in Indian cities but never trusted the numbers. So I built a pipeline to collect the real data myself.

Every 6 hours, it pulls live AQI readings from 25 cities, cleans and validates the data, loads it into PostgreSQL, and updates a Streamlit dashboard automatically.

---

## What I found

- Agra was consistently the most polluted — worse than Delhi on most days
- 68% of cities had Moderate to Hazardous air quality
- Coimbatore and Kochi had the cleanest air in the dataset
- The data told a very different story than the headlines

---

## How it works

| Step | File | What it does |
|------|------|-------------|
| Fetch | `fetch_aqi.py` | Pulls live data from Open-Meteo API for 25 cities |
| Clean | `clean_aqi.py` | Removes nulls, assigns pollution labels |
| Validate | `data_quality.py` | Runs 6 automated data quality checks |
| Load | `load_to_postgres.py` | Upserts records into PostgreSQL |
| Schedule | `scheduler.py` | Runs everything every 6 hours automatically |
| Export | `export_excel.py` | Generates Excel report with summary sheet |
| Dashboard | `dashboard/app.py` | Live Streamlit dashboard with KPIs and charts |

---

## Tech Stack

Python · Pandas · PostgreSQL · SQLAlchemy · Streamlit · Power BI · Tableau · Plotly · REST API · Excel

---

## Run it yourself

---

## Project Structure

src/
├── ingestion/fetch_aqi.py         # API collection
├── transformation/clean_aqi.py    # Cleaning & labeling
├── transformation/data_quality.py # Quality checks
├── loading/load_to_postgres.py    # PostgreSQL loading
├── scheduler.py                   # Automation
├── export_excel.py                # Excel reports
└── logger.py                      # Logging
sql/analysis_queries.py            # 7 SQL queries
dashboard/app.py                   # Streamlit dashboard

```bash
git clone https://github.com/saithrishadaggupati/environmental-data-pipeline.git
pip install -r requirements.txt
cp .env.example .env  # add your PostgreSQL credentials
python -m src.scheduler
streamlit run dashboard/app.py