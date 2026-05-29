import pandas as pd
import os
from src.logger import logger


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
    logger.info("Air quality labels assigned successfully")

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/clean_aqi.csv", index=False)
    logger.info(f"Cleaned data saved — {len(df)} rows written to data/processed/clean_aqi.csv")

    return df


if __name__ == "__main__":
    clean_data()