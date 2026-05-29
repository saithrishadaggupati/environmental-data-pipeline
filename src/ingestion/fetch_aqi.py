import requests
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
from src.logger import logger

load_dotenv()

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


def get_air_quality_label(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 200:
        return "Unhealthy"
    else:
        return "Hazardous"


def fetch_all_cities():
    logger.info(f"Starting AQI data pipeline for {len(CITIES)} cities")
    results = []
    failed = []

    for city in CITIES:
        try:
            url = (
                f"https://air-quality-api.open-meteo.com/v1/air-quality"
                f"?latitude={city['lat']}&longitude={city['lon']}"
                f"&current=pm2_5,pm10,carbon_monoxide,european_aqi"
            )
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            current = data["current"]

            results.append({
                "city": city["name"],
                "aqi_index": current["european_aqi"],
                "pm2_5": current["pm2_5"],
                "pm10": current["pm10"],
                "co": current["carbon_monoxide"],
                "air_quality_label": get_air_quality_label(current["european_aqi"]),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            logger.info(f"Fetched {city['name']} — AQI: {current['european_aqi']}")

        except Exception as e:
            logger.error(f"Failed to fetch {city['name']}: {e}")
            failed.append(city["name"])

    df = pd.DataFrame(results)

    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/aqi_data.csv", index=False)
    logger.info("CSV saved to data/raw/aqi_data.csv")

    if failed:
        logger.warning(f"Pipeline completed with {len(failed)} failed cities: {failed}")
    else:
        logger.info(f"Pipeline completed successfully. {len(results)}/{len(CITIES)} cities fetched.")

    return df


if __name__ == "__main__":
    fetch_all_cities()