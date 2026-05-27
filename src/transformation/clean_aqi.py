import pandas as pd
import os

# Read the raw data
df = pd.read_csv("data/raw/aqi_data.csv")

print("Raw data:")
print(df)

# Drop any rows with missing values
df = df.dropna()

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

# Save cleaned data
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/clean_aqi.csv", index=False)

print("\nCleaned data:")
print(df)
print("\nSaved to data/processed/clean_aqi.csv ✅")