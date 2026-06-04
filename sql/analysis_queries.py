import pandas as pd
import os
from src.logger import logger


def run_analysis():
    logger.info("Starting SQL analysis on AQI dataset")

    df = pd.read_csv("data/raw/aqi_data.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Query 1 — Top 5 most polluted cities
    logger.info("Running Query 1 — Most polluted cities")
    df1 = df.sort_values("aqi_index", ascending=False).head(5)[["city", "aqi_index", "air_quality_label"]]
    print("\n🏙️ Top 5 Most Polluted Cities:")
    print(df1.to_string(index=False))

    # Query 2 — Average AQI by pollution category
    logger.info("Running Query 2 — Average AQI by category")
    df2 = df.groupby("air_quality_label").agg(
        total_cities=("city", "count"),
        avg_aqi=("aqi_index", "mean")
    ).round(2).reset_index().sort_values("avg_aqi", ascending=False)
    print("\n📊 Average AQI by Category:")
    print(df2.to_string(index=False))

    # Query 3 — Cities above danger threshold
    logger.info("Running Query 3 — Cities above danger threshold")
    df3 = df[df["aqi_index"] > 200].sort_values("aqi_index", ascending=False)[["city", "aqi_index", "air_quality_label"]]
    print("\n⚠️ Cities Above Danger Threshold (AQI > 200):")
    print(df3.to_string(index=False))

    # Query 4 — Clean vs polluted ratio
    logger.info("Running Query 4 — Clean vs polluted city ratio")
    df["status"] = df["air_quality_label"].apply(lambda x: "Clean" if x == "Good" else "Polluted")
    df4 = df.groupby("status").agg(cities=("city", "count")).reset_index()
    df4["percentage"] = (df4["cities"] * 100.0 / df4["cities"].sum()).round(1)
    print("\n✅ Clean vs Polluted City Breakdown:")
    print(df4.to_string(index=False))

    # Query 5 — City rankings
    logger.info("Running Query 5 — City pollution rankings")
    df5 = df.sort_values("aqi_index", ascending=False).copy()
    df5["pollution_rank"] = df5["aqi_index"].rank(ascending=False, method="min").astype(int)
    df5["national_avg"] = round(df["aqi_index"].mean(), 2)
    print("\n🏆 City Pollution Rankings vs National Average:")
    print(df5[["city", "aqi_index", "air_quality_label", "pollution_rank", "national_avg"]].to_string(index=False))

    # Query 6 — High risk city analysis
    logger.info("Running Query 6 — High risk city analysis")
    def risk(aqi):
        if aqi > 200: return "High Risk"
        elif aqi > 100: return "Moderate Risk"
        else: return "Low Risk"
    df["risk_level"] = df["aqi_index"].apply(risk)
    df6 = df.groupby("risk_level").agg(
        total_cities=("city", "count"),
        avg_aqi=("aqi_index", "mean"),
        example_city=("city", "first")
    ).round(2).reset_index().sort_values("avg_aqi", ascending=False)
    print("\n🔴 Risk Level Distribution:")
    print(df6.to_string(index=False))

    # Query 7 — City Tier Analysis
    logger.info("Running Query 7 — City tier pollution comparison")
    metro = ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad']
    tier2 = ['Pune', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Surat', 'Nagpur']
    def tier(city):
        if city in metro: return "Metro"
        elif city in tier2: return "Tier-2"
        else: return "Tier-3"
    df["city_tier"] = df["city"].apply(tier)
    df7 = df.groupby("city_tier").agg(
        total_cities=("city", "count"),
        avg_aqi=("aqi_index", "mean"),
        worst_aqi=("aqi_index", "max"),
        best_aqi=("aqi_index", "min")
    ).round(2).reset_index().sort_values("avg_aqi", ascending=False)
    print("\n🏙️ Pollution by City Tier (Metro vs Tier-2 vs Tier-3):")
    print(df7.to_string(index=False))

    # Query 8 — Time of Day Analysis
    logger.info("Running Query 8 — Time of day AQI analysis")
    def time_of_day(hour):
        if 5 <= hour < 12: return "Morning (5-12)"
        elif 12 <= hour < 17: return "Afternoon (12-17)"
        elif 17 <= hour < 21: return "Evening (17-21)"
        else: return "Night (21-5)"
    df["hour"] = df["timestamp"].dt.hour
    df["time_of_day"] = df["hour"].apply(time_of_day)
    df8 = df.groupby("time_of_day").agg(
        total_readings=("aqi_index", "count"),
        avg_aqi=("aqi_index", "mean"),
        max_aqi=("aqi_index", "max"),
        min_aqi=("aqi_index", "min")
    ).round(2).reset_index().sort_values("avg_aqi", ascending=False)
    print("\n🕐 AQI by Time of Day:")
    print(df8.to_string(index=False))


if __name__ == "__main__":
    run_analysis()