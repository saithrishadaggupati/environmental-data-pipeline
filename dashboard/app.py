import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="India AQI Dashboard", layout="wide")
st.title("🌍 India Air Quality Dashboard")
st.caption("Live data from 25 Indian cities — updated every 6 hours")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

# Load data
df = pd.read_sql("SELECT * FROM aqi_readings", conn)
conn.close()

# Latest reading per city
latest = df.sort_values("timestamp").groupby("city").last().reset_index()

# KPI cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏙️ Cities Tracked", len(latest))
col2.metric("😷 Most Polluted", latest.loc[latest['aqi_index'].idxmax(), 'city'])
col3.metric("🌿 Cleanest City", latest.loc[latest['aqi_index'].idxmin(), 'city'])
col4.metric("⚠️ Hazardous Cities", len(latest[latest['air_quality_label'] == 'Hazardous']))

# Bar chart
st.subheader("📊 AQI by City")
latest_sorted = latest.sort_values("aqi_index", ascending=False)
fig1 = px.bar(
    latest_sorted,
    x="city",
    y="aqi_index",
    color="air_quality_label",
    title="AQI Levels Across Indian Cities",
    labels={"aqi_index": "AQI Index", "city": "City"}
)
st.plotly_chart(fig1, use_container_width=True)

# Pollution category breakdown
st.subheader("🥧 Pollution Category Breakdown")
category_counts = latest['air_quality_label'].value_counts().reset_index()
category_counts.columns = ['Category', 'Cities']
fig2 = px.pie(
    category_counts,
    names='Category',
    values='Cities',
    title='Cities by Air Quality Category'
)
st.plotly_chart(fig2, use_container_width=True)

# Data table
st.subheader("📋 Full Data Table")
st.dataframe(latest_sorted[["city","aqi_index","pm2_5","pm10","co","air_quality_label","timestamp"]])