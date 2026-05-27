import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="India AQI Dashboard", layout="wide")
st.title("🌍 India Air Quality Dashboard")
st.caption("Live data from 25 Indian cities")

# Load data from database
conn = sqlite3.connect("data/aqi_database.db")
df = pd.read_sql("SELECT * FROM aqi_readings", conn)
conn.close()

# Latest reading per city
latest = df.sort_values("timestamp").groupby("city").last().reset_index()

# KPI cards at top
col1, col2, col3 = st.columns(3)
col1.metric("🏙️ Cities Tracked", len(latest))
col2.metric("😷 Most Polluted", latest.loc[latest['aqi_index'].idxmax(), 'city'])
col3.metric("🌿 Cleanest City", latest.loc[latest['aqi_index'].idxmin(), 'city'])

# Bar chart
st.subheader("📊 AQI by City")
latest_sorted = latest.sort_values("aqi_index", ascending=False)
st.bar_chart(latest_sorted.set_index("city")["aqi_index"])

# Data table
st.subheader("📋 Full Data Table")
st.dataframe(latest_sorted[["city","aqi_index","pm2_5","pm10","co","timestamp"]])