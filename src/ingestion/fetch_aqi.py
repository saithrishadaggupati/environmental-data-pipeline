import requests
import pandas as pd
import os
import sqlite3
from datetime import datetime

CITIES = [
    {"name": "Visakhapatnam", "lat": 17.6868, "lon": 83.2185},
    {"name": "Bangalore", "lat": 12.9716, "lon": 77.5946},
    {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"name": "Pune", "lat": 18.5204, "lon": 73.8567},
    {"name": "Delhi", "lat": 28.6139, "lon": 77.2090},
    {"name": "Chennai", "lat": 13.0827, "lon": 80.2707},
    {"name": "Kolkata", "lat": 22.5726, "lon": 88.3639},
    {"name": "Hyderabad", "lat": 17.3850, "lon": 78.4867},
    {"name": "Ahmedabad", "lat": 23.0225, "lon": 72.5714},
    {"name": "Jaipur", "lat": 26.9124, "lon": 75.7873},
    {"name": "Lucknow", "lat": 26.8467, "lon": 80.9462},
    {"name": "Bhopal", "lat": 23.2599, "lon": 77.4126},
    {"name": "Nagpur", "lat": 21.1458, "lon": 79.0882},
    {"name": "Patna", "lat": 25.5941, "lon": 85.1376},
    {"name": "Indore", "lat": 22.7196, "lon": 75.8577},
    {"name": "Surat", "lat": 21.1702, "lon": 72.8311},
    {"name": "Coimbatore", "lat": 11.0168, "lon": 76.9558},
    {"name": "Kochi", "lat": 9.9312, "lon": 76.2673},
    {"name": "Chandigarh", "lat": 30.7333, "lon": 76.7794},
    {"name": "Varanasi", "lat": 25.3176, "lon": 82.9739},
    {"name": "Agra", "lat": 27.1767, "lon": 78.0081},
    {"name": "Ranchi", "lat": 23.3441, "lon": 85.3096},
    {"name": "Mysore", "lat": 12.2958, "lon": 76.6394},
    {"name": "Guwahati", "lat": 26.1445, "lon": 91.7362},
    {"name": "Bhubaneswar", "lat": 20.2961, "lon": 85.8245},
]

def save_to_database(df):
    """Save data to SQLite database"""
    # Create data folder if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Connect to database (creates it if it doesn't exist)
    conn = sqlite3.connect("data/aqi_database.db")
    
    # Save dataframe to SQL table
    # if_exists='append' means it ADDS new data each time (doesn't overwrite)
    df.to_sql("aqi_readings", conn, if_exists="append", index=False)
    
    conn.close()
    print("✅ Data saved to SQLite database: data/aqi_database.db")

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
        print(f"✅ Fetched: {city['name']}")

    df = pd.DataFrame(results)

    # Save BOTH ways
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/aqi_data.csv", index=False)
    print("\n✅ CSV saved!")

    save_to_database(df)  # NEW — saves to database too

    print("\n📊 Preview:")
    print(df[["city", "aqi_index", "pm2_5"]].head())
    return df

fetch_all_cities()