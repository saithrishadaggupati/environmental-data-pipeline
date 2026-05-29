# Air Quality Analytics Pipeline

I built this<img width="1814" height="784" alt="image" src="https://github.com/user-attachments/assets/166e2e5c-d509-4863-93e7-94b8ee8774f4" />

because I wanted to understand what an actual 
data pipeline looks like end to end — not just cleaning a 
CSV file, but the whole thing: pulling live data from an API, 
processing it, and getting it into a dashboard someone could 
actually use.

The project tracks air quality across 5 Indian cities in 
real time, classifies pollution levels by risk category, 
and displays everything in an interactive dashboard.

## Live App
👉 [Open Dashboard](https://environmental-data-pipeline-2dnkog5rys5suebnkpqyzv.streamlit.app)

## How it works

**1. Data Collection**
Pulls live AQI readings from a public REST API for 
cities including Delhi, Mumbai, Chennai, Kolkata, 
and Hyderabad.

**2. Processing**
Cleans the raw data with Pandas — handles missing 
values, standardizes formats, and classifies each 
reading into risk buckets (Good / Moderate / 
Unhealthy / Hazardous).

**3. Dashboard**
A Streamlit app that shows current AQI levels, 
city comparisons, and trend lines using Plotly charts.

## Tech used
Python · Pandas · Streamlit · Plotly · REST API

## Run it yourself
git clone https://github.com/saithrishadaggupati/environmental-data-pipeline
pip install -r requirements.txt
streamlit run dashboard/app.py

## Project structure
environmental-data-pipeline/
├── dashboard/      # Streamlit app
├── data/           # Raw and processed data
├── src/            # Pipeline scripts
├── .env.example    # Environment variable template
└── requirements.txt
