import pandas as pd
import numpy as np
from src.logger import logger

def run_statistical_analysis():
    logger.info("Starting statistical analysis on AQI dataset")
    
    df = pd.read_csv("data/processed/clean_aqi.csv")

    print("\n📊 Descriptive Statistics — AQI Index")
    print(f"  Mean AQI:      {df['aqi_index'].mean():.2f}")
    print(f"  Median AQI:    {df['aqi_index'].median():.2f}")
    print(f"  Std Dev:       {df['aqi_index'].std():.2f}")
    print(f"  Min AQI:       {df['aqi_index'].min():.2f}")
    print(f"  Max AQI:       {df['aqi_index'].max():.2f}")

    print("\n📈 Correlation Analysis")
    corr = df[['aqi_index','pm2_5','pm10','co']].corr()
    print(corr.round(2))

    print("\n🔍 Outlier Detection (Z-Score Method)")
    df['z_score'] = (df['aqi_index'] - df['aqi_index'].mean()) / df['aqi_index'].std()
    outliers = df[df['z_score'].abs() > 2][['city','aqi_index','z_score']]
    if len(outliers) > 0:
        print(outliers.to_string(index=False))
    else:
        print("  No outliers detected")

    print("\n📉 Percentile Distribution")
    print(f"  25th percentile: {df['aqi_index'].quantile(0.25):.2f}")
    print(f"  50th percentile: {df['aqi_index'].quantile(0.50):.2f}")
    print(f"  75th percentile: {df['aqi_index'].quantile(0.75):.2f}")
    print(f"  90th percentile: {df['aqi_index'].quantile(0.90):.2f}")

    logger.info("Statistical analysis complete")

run_statistical_analysis()