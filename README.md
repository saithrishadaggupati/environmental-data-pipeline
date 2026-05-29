# Environmental Air Quality Pipeline

I built this project because air quality data in India 
is scattered, hard to access, and rarely visualized 
in one place. This pipeline fixes that.

It automatically pulls live AQI readings across 25 Indian 
cities every 6 hours, cleans the data, stores it in 
PostgreSQL, and surfaces it in an interactive dashboard.

## What the data shows

After processing 25 cities:
- 8% of cities recorded Hazardous air quality
- 68% of cities showed poor air quality (Moderate/Unhealthy/Hazardous)
- Only 32% of cities had Good air quality
- Agra was the most polluted. Mumbai was the cleanest.

## How it works

1. fetch_aqi.py — calls a live REST API for 25 cities
2. clean_aqi.py — removes nulls, classifies pollution levels
3. load_to_postgres.py — stores clean data in PostgreSQL
4. scheduler.py — runs the full pipeline every 6 hours
5. dashboard/app.py — Streamlit dashboard with live KPIs

## Tech Stack

Python, Pandas, PostgreSQL, psycopg2, REST API, Streamlit

## Setup

1. Clone this repo
2. Copy .env.example to .env and add your credentials
3. pip install -r requirements.txt
4. python src/loading/load_to_postgres.py
5. python src/scheduler.py
6. python -m streamlit run dashboard/app.py