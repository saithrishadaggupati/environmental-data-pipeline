import requests
import pandas as pd
import os
import time
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
    {"name": "Amritsar", "lat": 31.6340, "lon": 74.8723},
    {"name": "Ludhiana", "lat": 30.9010, "lon": 75.8573},
    {"name": "Jodhpur", "lat": 26.2389, "lon": 73.0243},
    {"name": "Udaipur", "lat": 24.5854, "lon": 73.7125},
    {"name": "Kota", "lat": 25.2138, "lon": 75.8648},
    {"name": "Thiruvananthapuram", "lat": 8.5241, "lon": 76.9366},
    {"name": "Kozhikode", "lat": 11.2588, "lon": 75.7804},
    {"name": "Thrissur", "lat": 10.5276, "lon": 76.2144},
    {"name": "Madurai", "lat": 9.9252, "lon": 78.1198},
    {"name": "Tiruchirappalli", "lat": 10.7905, "lon": 78.7047},
    {"name": "Salem", "lat": 11.6643, "lon": 78.1460},
    {"name": "Tirunelveli", "lat": 8.7139, "lon": 77.7567},
    {"name": "Vijayawada", "lat": 16.5062, "lon": 80.6480},
    {"name": "Guntur", "lat": 16.3067, "lon": 80.4365},
    {"name": "Nellore", "lat": 14.4426, "lon": 79.9865},
    {"name": "Warangal", "lat": 17.9784, "lon": 79.5941},
    {"name": "Rajkot", "lat": 22.3039, "lon": 70.8022},
    {"name": "Vadodara", "lat": 22.3072, "lon": 73.1812},
    {"name": "Nashik", "lat": 19.9975, "lon": 73.7898},
    {"name": "Aurangabad", "lat": 19.8762, "lon": 75.3433},
    {"name": "Solapur", "lat": 17.6805, "lon": 75.9064},
    {"name": "Kolhapur", "lat": 16.7050, "lon": 74.2433},
    {"name": "Jabalpur", "lat": 23.1815, "lon": 79.9864},
    {"name": "Gwalior", "lat": 26.2183, "lon": 78.1828},
    {"name": "Raipur", "lat": 21.2514, "lon": 81.6296},
    {"name": "Bilaspur", "lat": 22.0797, "lon": 82.1391},
    {"name": "Dehradun", "lat": 30.3165, "lon": 78.0322},
    {"name": "Haridwar", "lat": 29.9457, "lon": 78.1642},
    {"name": "Meerut", "lat": 28.9845, "lon": 77.7064},
    {"name": "Kanpur", "lat": 26.4499, "lon": 80.3319},
    {"name": "Allahabad", "lat": 25.4358, "lon": 81.8463},
    {"name": "Gorakhpur", "lat": 26.7606, "lon": 83.3732},
    {"name": "Aligarh", "lat": 27.8974, "lon": 78.0880},
    {"name": "Bareilly", "lat": 28.3670, "lon": 79.4304},
    {"name": "Moradabad", "lat": 28.8386, "lon": 78.7733},
    {"name": "Saharanpur", "lat": 29.9640, "lon": 77.5460},
    {"name": "Faridabad", "lat": 28.4089, "lon": 77.3178},
    {"name": "Gurgaon", "lat": 28.4595, "lon": 77.0266},
    {"name": "Noida", "lat": 28.5355, "lon": 77.3910},
    {"name": "Agartala", "lat": 23.8315, "lon": 91.2868},
    {"name": "Shillong", "lat": 25.5788, "lon": 91.8933},
    {"name": "Imphal", "lat": 24.8170, "lon": 93.9368},
    {"name": "Aizawl", "lat": 23.7271, "lon": 92.7176},
    {"name": "Kohima", "lat": 25.6701, "lon": 94.1077},
    {"name": "Itanagar", "lat": 27.0844, "lon": 93.6053},
    {"name": "Gangtok", "lat": 27.3314, "lon": 88.6138},
    {"name": "Panaji", "lat": 15.4909, "lon": 73.8278},
    {"name": "Shimla", "lat": 31.1048, "lon": 77.1734},
    {"name": "Jammu", "lat": 32.7266, "lon": 74.8570},
    {"name": "Srinagar", "lat": 34.0837, "lon": 74.7973},
    {"name": "Leh", "lat": 34.1526, "lon": 77.5771},
    {"name": "Mangalore", "lat": 12.9141, "lon": 74.8560},
    {"name": "Hubli", "lat": 15.3647, "lon": 75.1240},
    {"name": "Belgaum", "lat": 15.8497, "lon": 74.4977},
    {"name": "Gulbarga", "lat": 17.3297, "lon": 76.8343},
    {"name": "Davangere", "lat": 14.4644, "lon": 75.9218},
    {"name": "Bellary", "lat": 15.1394, "lon": 76.9214},
    {"name": "Bikaner", "lat": 28.0229, "lon": 73.3119},
    {"name": "Ajmer", "lat": 26.4499, "lon": 74.6399},
    {"name": "Sikar", "lat": 27.6094, "lon": 75.1399},
    {"name": "Bhilwara", "lat": 25.3407, "lon": 74.6313},
    {"name": "Dhanbad", "lat": 23.7957, "lon": 86.4304},
    {"name": "Jamshedpur", "lat": 22.8046, "lon": 86.2029},
    {"name": "Bokaro", "lat": 23.6693, "lon": 86.1511},
    {"name": "Durgapur", "lat": 23.5204, "lon": 87.3119},
    {"name": "Asansol", "lat": 23.6739, "lon": 86.9524},
    {"name": "Siliguri", "lat": 26.7271, "lon": 88.3953},
    {"name": "Cuttack", "lat": 20.4625, "lon": 85.8830},
    {"name": "Rourkela", "lat": 22.2604, "lon": 84.8536},
    {"name": "Berhampur", "lat": 19.3150, "lon": 84.7941},
    {"name": "Tirupati", "lat": 13.6288, "lon": 79.4192},
    {"name": "Kakinada", "lat": 16.9891, "lon": 82.2475},
    {"name": "Rajahmundry", "lat": 17.0005, "lon": 81.8040},
    {"name": "Anantapur", "lat": 14.6819, "lon": 77.6006},
    {"name": "Nizamabad", "lat": 18.6725, "lon": 78.0941},
    {"name": "Karimnagar", "lat": 18.4386, "lon": 79.1288},
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
        max_retries = 3
        for attempt in range(max_retries):
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
                    "lat": city["lat"],
                    "lon": city["lon"],
                    "aqi_index": current["european_aqi"],
                    "pm2_5": current["pm2_5"],
                    "pm10": current["pm10"],
                    "co": current["carbon_monoxide"],
                    "air_quality_label": get_air_quality_label(current["european_aqi"]),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                logger.info(f"Fetched {city['name']} — AQI: {current['european_aqi']}")
                break

            except Exception as e:
                logger.warning(f"Attempt {attempt+1} failed for {city['name']}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    logger.error(f"All 3 attempts failed for {city['name']}")
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