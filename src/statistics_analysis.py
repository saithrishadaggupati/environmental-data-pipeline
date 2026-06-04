import pandas as pd
import numpy as np
from scipy import stats
from src.logger import logger


NORTH_CITIES = [
    "Delhi", "Agra", "Lucknow", "Kanpur", "Varanasi", "Patna",
    "Jaipur", "Jodhpur", "Amritsar", "Chandigarh", "Ludhiana",
    "Meerut", "Allahabad", "Ghaziabad", "Faridabad", "Noida"
]

SOUTH_CITIES = [
    "Chennai", "Bangalore", "Hyderabad", "Kochi", "Coimbatore",
    "Thiruvananthapuram", "Madurai", "Visakhapatnam", "Vijayawada",
    "Mysuru", "Mangalore", "Tiruchirappalli"
]


def run_statistical_analysis():
    logger.info("Starting statistical analysis on AQI dataset")

    df = pd.read_csv("data/processed/clean_aqi.csv")

    # ── Descriptive statistics ─────────────────────────────────────────────────
    print("\n📊 Descriptive Statistics — AQI Index")
    print(f"  Mean AQI      : {df['aqi_index'].mean():.2f}")
    print(f"  Median AQI    : {df['aqi_index'].median():.2f}")
    print(f"  Std Dev       : {df['aqi_index'].std():.2f}")
    print(f"  Min AQI       : {df['aqi_index'].min():.2f}")
    print(f"  Max AQI       : {df['aqi_index'].max():.2f}")
    print(f"  Skewness      : {df['aqi_index'].skew():.4f}")
    print(f"  Kurtosis      : {df['aqi_index'].kurt():.4f}")

    # ── Percentile distribution ────────────────────────────────────────────────
    print("\n📉 Percentile Distribution")
    for p in [25, 50, 75, 90, 95]:
        print(f"  {p}th percentile : {df['aqi_index'].quantile(p / 100):.2f}")

    # ── Outlier detection ──────────────────────────────────────────────────────
    print("\n🔍 Outlier Detection (Z-Score Method, threshold = 2)")
    df["z_score"] = (df["aqi_index"] - df["aqi_index"].mean()) / df["aqi_index"].std()
    outliers = df[df["z_score"].abs() > 2][["city", "aqi_index", "z_score"]]
    if len(outliers) > 0:
        print(outliers.to_string(index=False))
    else:
        print("  No outliers detected")

    # ── AQI label distribution ─────────────────────────────────────────────────
    print("\n📋 AQI Category Distribution")
    if "air_quality_label" in df.columns:
        dist = df["air_quality_label"].value_counts()
        for label, count in dist.items():
            pct = round(count / len(df) * 100, 1)
            print(f"  {label:<12} : {count} cities ({pct}%)")

    # ── North vs South hypothesis test ────────────────────────────────────────
    print("\n🧪 Hypothesis Test — North India vs South India AQI")
    print("   H0: No significant difference in mean AQI between north and south")
    print("   Test: Mann-Whitney U (non-parametric, does not assume normal distribution)")

    north_aqi = df[df["city"].isin(NORTH_CITIES)]["aqi_index"].dropna().values
    south_aqi = df[df["city"].isin(SOUTH_CITIES)]["aqi_index"].dropna().values

    if len(north_aqi) > 0 and len(south_aqi) > 0:
        u_stat, p_value = stats.mannwhitneyu(north_aqi, south_aqi, alternative="greater")
        print(f"\n  North cities  : {len(north_aqi)} matched  |  mean AQI = {north_aqi.mean():.2f}")
        print(f"  South cities  : {len(south_aqi)} matched  |  mean AQI = {south_aqi.mean():.2f}")
        print(f"  U-statistic   : {round(u_stat, 4)}")
        print(f"  p-value       : {round(p_value, 6)}")

        if p_value < 0.05:
            print("  ✅ Statistically significant (p < 0.05)")
            print("     → North India has significantly higher AQI than South India")
        else:
            print("  ❌ Not statistically significant (p ≥ 0.05)")
            print("     → No reliable AQI difference detected between regions")
    else:
        print(f"  ⚠️  Not enough matched cities — north: {len(north_aqi)}, south: {len(south_aqi)}")
        print("     → Check that city names in the dataset match the lists above")

    # ── Top and bottom 5 cities ────────────────────────────────────────────────
    print("\n🏙️  Top 5 Most Polluted Cities")
    top5 = df.nlargest(5, "aqi_index")[["city", "aqi_index", "air_quality_label"]] if "air_quality_label" in df.columns else df.nlargest(5, "aqi_index")[["city", "aqi_index"]]
    print(top5.to_string(index=False))

    print("\n🌿 Top 5 Cleanest Cities")
    bottom5 = df.nsmallest(5, "aqi_index")[["city", "aqi_index", "air_quality_label"]] if "air_quality_label" in df.columns else df.nsmallest(5, "aqi_index")[["city", "aqi_index"]]
    print(bottom5.to_string(index=False))

    logger.info("Statistical analysis complete")


if __name__ == "__main__":
    run_statistical_analysis()