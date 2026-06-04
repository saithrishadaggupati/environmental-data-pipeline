import pandas as pd
import os
from src.logger import logger


# City tier classification based on Census 2011 population data
# Metro: population > 4 million
# Tier-1: population 1–4 million
# Tier-2: population 0.5–1 million
# Tier-3: population < 0.5 million
CITY_POPULATION = {
    "Delhi": 11034555, "Mumbai": 12442373, "Kolkata": 4496694,
    "Chennai": 4646732, "Bangalore": 8443675, "Hyderabad": 6809970,
    "Ahmedabad": 5577940, "Pune": 3124458, "Surat": 4467797,
    "Jaipur": 3046163, "Lucknow": 2817105, "Kanpur": 2767031,
    "Nagpur": 2405421, "Indore": 1964086, "Bhopal": 1798218,
    "Patna": 1684222, "Vadodara": 1666703, "Ghaziabad": 1648643,
    "Ludhiana": 1618879, "Agra": 1574542, "Nashik": 1486053,
    "Faridabad": 1414050, "Meerut": 1305429, "Rajkot": 1286678,
    "Varanasi": 1201815, "Srinagar": 1180570, "Aurangabad": 1171330,
    "Amritsar": 1132761, "Allahabad": 1117094, "Visakhapatnam": 1728128,
    "Coimbatore": 1050721, "Gurgaon": 876824, "Noida": 642381,
    "Kochi": 601574, "Chandigarh": 960787, "Jabalpur": 1267564,
    "Gwalior": 1054420, "Jodhpur": 1033918, "Madurai": 1017865,
    "Raipur": 1010087, "Kota": 1001365, "Ranchi": 1073440,
    "Thiruvananthapuram": 957730, "Tiruchirappalli": 916857,
    "Bhubaneswar": 837737, "Warangal": 811844, "Vijayawada": 1048240,
    "Mysore": 887446, "Dehradun": 578420, "Jammu": 503690,
    "Mangalore": 484785, "Guntur": 647508, "Bikaner": 647804,
    "Tirupati": 459985, "Ajmer": 542580, "Dhanbad": 1162472,
    "Jamshedpur": 631069, "Solapur": 951558, "Hubli": 943788,
    "Moradabad": 889810, "Bareilly": 898167, "Aligarh": 872575,
    "Gorakhpur": 673446, "Saharanpur": 703345, "Kolhapur": 549236,
    "Bilaspur": 330058, "Asansol": 1243414, "Durgapur": 566937,
    "Siliguri": 513264, "Cuttack": 606007, "Bokaro": 563417,
    "Rourkela": 272984, "Berhampur": 355823, "Nellore": 538523,
    "Kakinada": 313071, "Rajahmundry": 341831, "Karimnagar": 261185,
    "Nizamabad": 311152, "Anantapur": 276033, "Haridwar": 228832,
    "Udaipur": 451100, "Shimla": 169578, "Leh": 30870,
    "Panaji": 114405, "Bhilwara": 340140, "Sikar": 237600,
    "Belgaum": 488157, "Gulbarga": 532031, "Davangere": 434708,
    "Bellary": 409644, "Tirunelveli": 473637, "Salem": 831038,
    "Kozhikode": 609224, "Thrissur": 315957, "Shillong": 143229,
    "Guwahati": 963429, "Agartala": 400004, "Imphal": 268243,
    "Aizawl": 293416, "Kohima": 99039, "Itanagar": 44981,
    "Gangtok": 100286,
}


def classify_tier(city):
    pop = CITY_POPULATION.get(city)
    if pop is None:
        return "Tier-3"
    elif pop >= 4_000_000:
        return "Metro"
    elif pop >= 1_000_000:
        return "Tier-1"
    elif pop >= 500_000:
        return "Tier-2"
    else:
        return "Tier-3"


def label_air(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 200:
        return "Unhealthy"
    else:
        return "Hazardous"


def clean_data():
    logger.info("Starting data transformation — reading raw AQI data")
    df = pd.read_csv("data/raw/aqi_data.csv")
    logger.info(f"Loaded {len(df)} rows from raw CSV")

    before = len(df)
    df = df.dropna()
    dropped = before - len(df)

    if dropped > 0:
        logger.warning(f"Dropped {dropped} rows with missing values")
    else:
        logger.info("No missing values found — data is clean")

    df["air_quality_label"] = df["aqi_index"].apply(label_air)
    df["city_tier"] = df["city"].apply(classify_tier)
    logger.info("Air quality labels and city tiers assigned successfully")

    tier_summary = df["city_tier"].value_counts().to_dict()
    logger.info(f"City tier distribution: {tier_summary}")

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/clean_aqi.csv", index=False)
    logger.info(f"Cleaned data saved — {len(df)} rows written to data/processed/clean_aqi.csv")

    return df


if __name__ == "__main__":
    clean_data()