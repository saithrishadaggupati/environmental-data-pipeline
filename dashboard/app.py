import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import plotly.express as px

load_dotenv()

st.set_page_config(page_title="India AQI Dashboard", layout="wide")

st.title("🌍 India AQI Dashboard")
st.caption("Live data from 25 Indian cities — refreshed every 6 hours")


@st.cache_data(ttl=3600)
def load_data():
    engine = create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    return pd.read_sql("SELECT * FROM aqi_readings", engine)


df = load_data()
latest = df.sort_values("timestamp").groupby("city").last().reset_index()

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏙️ Cities Tracked", len(latest))
col2.metric("😷 Most Polluted", latest.loc[latest["aqi_index"].idxmax(), "city"])
col3.metric("🌿 Cleanest City", latest.loc[latest["aqi_index"].idxmin(), "city"])
col4.metric("⚠️ Hazardous Cities", len(latest[latest["air_quality_label"] == "Hazardous"]))

# Bar Chart
st.subheader("📊 AQI by City")
latest_sorted = latest.sort_values("aqi_index", ascending=False)
fig1 = px.bar(
    latest_sorted,
    x="city",
    y="aqi_index",
    color="air_quality_label",
    title="AQI Levels Across Indian Cities",
    labels={"aqi_index": "AQI Index", "city": "City"},
    color_discrete_map={
        "Good": "green",
        "Moderate": "yellow",
        "Unhealthy": "orange",
        "Hazardous": "red"
    }
)
st.plotly_chart(fig1, use_container_width=True)

# Pie Chart
st.subheader("🥧 Pollution Category Breakdown")
category_counts = latest["air_quality_label"].value_counts().reset_index()
category_counts.columns = ["Category", "Cities"]
fig2 = px.pie(
    category_counts,
    names="Category",
    values="Cities",
    title="Cities by Air Quality Category",
    color_discrete_map={
        "Good": "green",
        "Moderate": "yellow",
        "Unhealthy": "orange",
        "Hazardous": "red"
    }
)
st.plotly_chart(fig2, use_container_width=True)

# Scatter Plot
st.subheader("📈 PM2.5 vs AQI")
fig3 = px.scatter(
    latest_sorted,
    x="pm2_5",
    y="aqi_index",
    color="air_quality_label",
    size="aqi_index",
    hover_name="city",
    title="PM2.5 vs AQI Index by City"
)
st.plotly_chart(fig3, use_container_width=True)

# Data Table
st.subheader("📋 Full Data Table")
st.dataframe(
    latest_sorted[["city", "aqi_index", "pm2_5", "pm10", "co", "air_quality_label", "timestamp"]]
)