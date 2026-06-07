import streamlit as st
import pandas as pd
import os
import plotly.express as px
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="India AQI Dashboard", layout="wide")

st.title("🌍 India AQI Dashboard")
st.caption("Live data from 100+ Indian cities — refreshed every 6 hours via GitHub Actions")


@st.cache_data(ttl=3600)
def load_data():
    csv_path = "data/raw/aqi_data.csv"
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        st.error("Data file not found. Pipeline may not have run yet.")
        return pd.DataFrame()


df = load_data()

if df.empty:
    st.stop()

latest = df.sort_values("timestamp").groupby("city").last().reset_index()
last_updated = df["timestamp"].max()
st.caption(f"🕐 Last updated: {last_updated}")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏙️ Cities Tracked", len(latest))
col2.metric("😷 Most Polluted", latest.loc[latest["aqi_index"].idxmax(), "city"])
col3.metric("🌿 Cleanest City", latest.loc[latest["aqi_index"].idxmin(), "city"])
col4.metric("⚠️ Hazardous Cities", len(latest[latest["air_quality_label"] == "Hazardous"]))

# India Map
st.subheader("🗺️ AQI Map of India")

COLOR_MAP = {
    "Good": "green", "Moderate": "orange",
    "Unhealthy": "red", "Hazardous": "darkred"
}

m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

for _, row in latest.iterrows():
    if pd.notna(row.get("lat")) and pd.notna(row.get("lon")):
        color = COLOR_MAP.get(row["air_quality_label"], "blue")
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=row["aqi_index"] / 20,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"{row['city']}: AQI {row['aqi_index']} ({row['air_quality_label']})"
        ).add_to(m)

st_folium(m, width=1200, height=500)

# Bar Chart
st.subheader("📊 AQI Levels — All Cities")
latest_sorted = latest.sort_values("aqi_index", ascending=False)
fig1 = px.bar(
    latest_sorted, x="city", y="aqi_index",
    color="air_quality_label",
    title=f"AQI Levels Across {len(latest)} Indian Cities",
    labels={"aqi_index": "AQI Index", "city": "City"},
    color_discrete_map={
        "Good": "green", "Moderate": "yellow",
        "Unhealthy": "orange", "Hazardous": "red"
    }
)
st.plotly_chart(fig1, use_container_width=True)

# Pie Chart
st.subheader("🥧 Pollution Category Breakdown")
category_counts = latest["air_quality_label"].value_counts().reset_index()
category_counts.columns = ["Category", "Cities"]
fig2 = px.pie(
    category_counts, names="Category", values="Cities",
    title="Cities by Air Quality Category",
    color_discrete_map={
        "Good": "green", "Moderate": "yellow",
        "Unhealthy": "orange", "Hazardous": "red"
    }
)
st.plotly_chart(fig2, use_container_width=True)

# Scatter
st.subheader("📈 PM2.5 vs AQI")
fig3 = px.scatter(
    latest_sorted, x="pm2_5", y="aqi_index",
    color="air_quality_label", size="aqi_index",
    hover_name="city", title="PM2.5 vs AQI Index"
)
st.plotly_chart(fig3, use_container_width=True)

# Trend
st.subheader("📉 AQI Trend Over Time")
if len(df) > len(latest):
    top_cities = latest.nlargest(5, "aqi_index")["city"].tolist()
    history_filtered = df[df["city"].isin(top_cities)]
    fig4 = px.line(
        history_filtered, x="timestamp", y="aqi_index",
        color="city", title="AQI Trend — Top 5 Most Polluted Cities"
    )
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.info("Trend data will appear after a few pipeline runs.")

# Table
st.subheader("📋 Full Data Table")
st.dataframe(
    latest_sorted[["city", "aqi_index", "pm2_5", "pm10", "co", "air_quality_label", "timestamp"]],
    use_container_width=True
)