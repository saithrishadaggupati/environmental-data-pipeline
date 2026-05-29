\# Environmental Air Quality Data Pipeline



I built this project because air quality keeps coming up in 

conversations about India's cities — but I was always reading 

headlines, never looking at the actual numbers. I wanted to 

change that.



So I built a pipeline that pulls live AQI readings across 25 

Indian cities every 6 hours, cleans and validates the data, 

stores it in PostgreSQL, and visualizes it in an interactive 

dashboard. It runs automatically — no manual work needed.



\## What the data actually showed



Going in, I expected the data to match the headlines. Some of 

it did — Agra consistently appeared among the most polluted 

cities, which surprised me since it rarely dominates pollution 

news. But several cities that never make national headlines 

showed stable, healthy air quality throughout.



That gap between headlines and data is exactly why I think 

projects like this matter. The story data tells is almost 

always more nuanced than what gets reported.



Key findings across 25 cities:

\- 68% of cities recorded Moderate to Hazardous air quality

\- Only 32% of cities met Good air quality standards

\- Agra recorded the highest pollution levels consistently

\- Mumbai recorded the cleanest air quality in the dataset



\## How the pipeline works



Raw API data goes through 4 stages before it reaches the dashboard:



1\. \*\*Fetch\*\* — fetch\_aqi.py calls a live REST API for all 25 cities

2\. \*\*Clean\*\* — clean\_aqi.py removes nulls and classifies pollution levels

3\. \*\*Validate\*\* — data\_quality.py runs automated checks and flags anomalies

4\. \*\*Load\*\* — load\_to\_postgres.py stores clean records in PostgreSQL

5\. \*\*Schedule\*\* — scheduler.py runs the full pipeline every 6 hours automatically

6\. \*\*Monitor\*\* — logger.py tracks every stage with structured logs and error tracking

7\. \*\*Visualize\*\* — Streamlit dashboard surfaces live KPIs, trends, and city breakdowns



\## Tech Stack



Python, Pandas, PostgreSQL, SQLite, REST API, Streamlit, 

Plotly, APScheduler, psycopg2, python-dotenv



\## Setup



1\. Clone this repo

2\. Copy `.env.example` to `.env` and add your database credentials

3\. `pip install -r requirements.txt`

4\. `python src/loading/load\_to\_postgres.py`

5\. `python src/scheduler.py`

6\. `streamlit run dashboard/app.py`



\## Project Structure

