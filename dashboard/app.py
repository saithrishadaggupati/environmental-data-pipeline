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

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏙️ Cities Tracked", len(latest))
col2.metric("😷 Most Polluted", latest.loc[latest["aqi_index"].idxmax(), "city"])
col3.metric("🌿 Cleanest City", latest.loc[latest["aqi_index"].idxmin(), "city"])
col4.metric("⚠️ Hazardous Cities", len(latest[latest["air_quality_label"] == "Hazardous"]))

# India Map
st.subheader("🗺️ AQI Map of India")

CITY_COORDS = {
    "Visakhapatnam": [17.6868, 83.2185], "Bangalore": [12.9716, 77.5946],
    "Mumbai": [19.0760, 72.8777], "Pune": [18.5204, 73.8567],
    "Delhi": [28.6139, 77.2090], "Chennai": [13.0827, 80.2707],
    "Kolkata": [22.5726, 88.3639], "Hyderabad": [17.3850, 78.4867],
    "Ahmedabad": [23.0225, 72.5714], "Jaipur": [26.9124, 75.7873],
    "Lucknow": [26.8467, 80.9462], "Bhopal": [23.2599, 77.4126],
    "Nagpur": [21.1458, 79.0882], "Patna": [25.5941, 85.1376],
    "Indore": [22.7196, 75.8577], "Surat": [21.1702, 72.8311],
    "Coimbatore": [11.0168, 76.9558], "Kochi": [9.9312, 76.2673],
    "Chandigarh": [30.7333, 76.7794], "Varanasi": [25.3176, 82.9739],
    "Agra": [27.1767, 78.0081], "Ranchi": [23.3441, 85.3096],
    "Mysore": [12.2958, 76.6394], "Guwahati": [26.1445, 91.7362],
    "Bhubaneswar": [20.2961, 85.8245], "Amritsar": [31.6340, 74.8723],
    "Ludhiana": [30.9010, 75.8573], "Jodhpur": [26.2389, 73.0243],
    "Udaipur": [24.5854, 73.7125], "Kota": [25.2138, 75.8648],
    "Thiruvananthapuram": [8.5241, 76.9366], "Kozhikode": [11.2588, 75.7804],
    "Thrissur": [10.5276, 76.2144], "Madurai": [9.9252, 78.1198],
    "Tiruchirappalli": [10.7905, 78.7047], "Salem": [11.6643, 78.1460],
    "Vijayawada": [16.5062, 80.6480], "Guntur": [16.3067, 80.4365],
    "Noida": [28.5355, 77.3910], "Gurgaon": [28.4595, 77.0266],
    "Faridabad": [28.4089, 77.3178], "Meerut": [28.9845, 77.7064],
    "Kanpur": [26.4499, 80.3319], "Dehradun": [30.3165, 78.0322],
    "Shimla": [31.1048, 77.1734], "Jammu": [32.7266, 74.8570],
    "Srinagar": [34.0837, 74.7973], "Mangalore": [12.9141, 74.8560],
    "Hubli": [15.3647, 75.1240], "Rajkot": [22.3039, 70.8022],
    "Vadodara": [22.3072, 73.1812], "Nashik": [19.9975, 73.7898],
    "Dhanbad": [23.7957, 86.4304], "Jamshedpur": [22.8046, 86.2029],
    "Durgapur": [23.5204, 87.3119], "Siliguri": [26.7271, 88.3953],
}

COLOR_MAP = {
    "Good": "green", "Moderate": "orange",
    "Unhealthy": "red", "Hazardous": "darkred"
}

m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

for _, row in latest.iterrows():
    city = row["city"]
    if city in CITY_COORDS:
        lat, lon = CITY_COORDS[city]
        color = COLOR_MAP.get(row["air_quality_label"], "blue")
        folium.CircleMarker(
            location=[lat, lon],
            radius=row["aqi_index"] / 20,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"{city}: AQI {row['aqi_index']} ({row['air_quality_label']})"
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