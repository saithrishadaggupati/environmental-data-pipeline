import pandas as pd
from src.logger import logger
from datetime import datetime, timedelta


def run_data_quality_checks(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Starting data quality checks...")
    issues = []

    # Check 1 — Null check
    null_cities = df[df['aqi_index'].isnull()]['city'].tolist()
    if null_cities:
        logger.warning(f"NULL AQI values found for: {null_cities}")
        issues.append(f"Null AQI: {null_cities}")
    else:
        logger.info("Null check passed")

    # Check 2 — Range check
    invalid = df[(df['aqi_index'] < 0) | (df['aqi_index'] > 500)]
    if not invalid.empty:
        logger.warning(f"Invalid AQI range for: {invalid['city'].tolist()}")
        issues.append(f"Invalid range: {invalid['city'].tolist()}")
    else:
        logger.info("Range check passed")

    # Check 3 — Duplicate check
    dupes = df[df.duplicated(subset=['city', 'timestamp'], keep=False)]
    if not dupes.empty:
        logger.warning(f"Duplicate records found: {len(dupes)} rows")
        issues.append(f"Duplicates: {len(dupes)} rows")
    else:
        logger.info("Duplicate check passed")

    # Check 4 — Freshness check
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        stale = df[df['timestamp'] < datetime.now() - timedelta(hours=8)]
        if not stale.empty:
            logger.warning(f"Stale data found for: {stale['city'].tolist()}")
            issues.append(f"Stale data: {stale['city'].tolist()}")
        else:
            logger.info("Freshness check passed")

    if issues:
        logger.warning(f"Data quality issues found: {len(issues)}")
    else:
        logger.info(f"All checks passed — {len(df)} rows validated")

    return df


if __name__ == "__main__":
    import os
    if os.path.exists("data/raw/aqi_data.csv"):
        df = pd.read_csv("data/raw/aqi_data.csv")
        run_data_quality_checks(df)
    else:
        logger.error("No data file found")