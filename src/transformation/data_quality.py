import pandas as pd
from src.logger import logger

def run_quality_checks(df):
    """
    Runs automated data quality checks on AQI pipeline data.
    Validates integrity, detects anomalies, and returns clean dataset.
    """
    logger.info("Starting automated data quality checks")
    total = len(df)
    issues = 0

    # Check 1 — Missing city names
    missing_cities = df['city'].isnull().sum()
    if missing_cities > 0:
        logger.warning(f"Data integrity issue — {missing_cities} rows have missing city names")
        df = df.dropna(subset=['city'])
        issues += missing_cities
    else:
        logger.info("Check 1 passed — no missing city names")

    # Check 2 — Invalid AQI values
    invalid_aqi = df[df['aqi_index'] < 0].shape[0]
    if invalid_aqi > 0:
        logger.warning(f"Anomaly detected — {invalid_aqi} rows have negative AQI values")
        df = df[df['aqi_index'] >= 0]
        issues += invalid_aqi
    else:
        logger.info("Check 2 passed — all AQI values are valid")

    # Check 3 — Duplicate cities
    duplicates = df.duplicated(subset=['city']).sum()
    if duplicates > 0:
        logger.warning(f"Duplicate records found — {duplicates} duplicate city entries removed")
        df = df.drop_duplicates(subset=['city'])
        issues += duplicates
    else:
        logger.info("Check 3 passed — no duplicate cities")

    # Check 4 — Missing AQI values
    missing_aqi = df['aqi_index'].isnull().sum()
    if missing_aqi > 0:
        logger.warning(f"Data integrity issue — {missing_aqi} rows have missing AQI values")
        df = df.dropna(subset=['aqi_index'])
        issues += missing_aqi
    else:
        logger.info("Check 4 passed — no missing AQI values")

    # Check 5 — AQI outliers (anomaly detection)
    outliers = df[df['aqi_index'] > 500].shape[0]
    if outliers > 0:
        logger.warning(f"Anomaly detected — {outliers} rows have unrealistic AQI values above 500")
        df = df[df['aqi_index'] <= 500]
        issues += outliers
    else:
        logger.info("Check 5 passed — no AQI outliers detected")

    # Check 6 — Validate air quality labels exist
    missing_labels = df['air_quality_label'].isnull().sum()
    if missing_labels > 0:
        logger.warning(f"Data integrity issue — {missing_labels} rows missing air quality labels")
        issues += missing_labels
    else:
        logger.info("Check 6 passed — all rows have air quality labels")

    # Final quality report
    logger.info(f"Data quality report — {total} records checked, {issues} issues found and resolved, {len(df)} clean records ready for analysis")

    return df

if __name__ == "__main__":
    df = pd.read_csv("data/processed/clean_aqi.csv")
    df = run_quality_checks(df)