import pandas as pd
import matplotlib.pyplot as plt

# Read the cleaned data
df = pd.read_csv("data/processed/clean_aqi.csv")

# Create the chart
plt.figure(figsize=(10, 6))
colors = []
for aqi in df["aqi_index"]:
    if aqi <= 50:
        colors.append("green")
    elif aqi <= 100:
        colors.append("yellow")
    elif aqi <= 200:
        colors.append("orange")
    else:
        colors.append("red")

plt.bar(df["city"], df["aqi_index"], color=colors)
plt.title("Air Quality Index by City")
plt.xlabel("City")
plt.ylabel("AQI Index")
plt.tight_layout()

# Save the chart as an image
plt.savefig("dashboard/aqi_chart.png")
print("Chart saved to dashboard/aqi_chart.png ✅")

plt.show()