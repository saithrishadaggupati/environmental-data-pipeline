import pandas as pd
import os
from src.logger import logger

# Read the raw data
logger.info("Starting data transformation — reading raw AQI data")
df = pd.read_csv("data/raw/aqi_data.csv")
logger.info(f"Loaded {len(df)} rows from raw CSV")

# Drop any rows with missing values
before = len(df)
df = df.dropna()
dropped = before - len(df)
if dropped > 0:
    logger.warning(f"Dropped {dropped} rows with missing values")
else:
    logger.info("No missing values found — data is clean")

# Add air quality label
def label_air(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 200:
        return "Unhealthy"
    else:
        return "Hazardous"

df["air_quality_label"] = df["aqi_index"].apply(label_air)
logger.info("Air quality labels assigned successfully")

# Save cleaned data
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/clean_aqi.csv", index=False)
logger.info(f"Cleaned data saved — {len(df)} rows written to data/processed/clean_aqi.csv")