import requests
import pandas as pd
import os
from datetime import datetime

CITIES = [
    {"name": "Visakhapatnam", "lat": 17.6868, "lon": 83.2185},
    {"name": "Bangalore", "lat": 12.9716, "lon": 77.5946},
    {"name": "Gujarat", "lat": 23.0225, "lon": 72.5714},
    {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"name": "Pune", "lat": 18.5204, "lon": 73.8567},
]

def fetch_all_cities():
    results = []
    for city in CITIES:
        url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={city['lat']}&longitude={city['lon']}&current=pm2_5,pm10,carbon_monoxide,european_aqi"
        response = requests.get(url)
        data = response.json()
        current = data["current"]
        results.append({
            "city": city["name"],
            "aqi_index": current["european_aqi"],
            "pm2_5": current["pm2_5"],
            "pm10": current["pm10"],
            "co": current["carbon_monoxide"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"Found: {city['name']} -> {city['lat']}, {city['lon']}")

    df = pd.DataFrame(results)
    print("\nData fetched successfully!")
    print(df)

    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/aqi_data.csv", index=False)
    print("\nData saved to data/raw/aqi_data.csv")

fetch_all_cities()