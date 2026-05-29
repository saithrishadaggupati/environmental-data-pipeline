import pandas as pd
import os
from src.logger import logger

def export_to_excel():
    logger.info("Starting Excel export")
    
    # Read cleaned data
    df = pd.read_csv("data/processed/clean_aqi.csv")
    
    # Create output folder
    os.makedirs("data/exports", exist_ok=True)
    
    # Export to Excel with formatting
    output_path = "data/exports/AQI_India_Report.xlsx"
    
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        
        # Sheet 1 — Full data
        df.to_excel(writer, sheet_name="All Cities", index=False)
        
        # Sheet 2 — Most polluted cities
        top_polluted = df.nlargest(10, "aqi_index")[["city", "aqi_index", "air_quality_label"]]
        top_polluted.to_excel(writer, sheet_name="Most Polluted", index=False)
        
        # Sheet 3 — Category summary
        summary = df.groupby("air_quality_label").agg(
            total_cities=("city", "count"),
            avg_aqi=("aqi_index", "mean"),
            max_aqi=("aqi_index", "max")
        ).round(2).reset_index()
        summary.to_excel(writer, sheet_name="Category Summary", index=False)
    
    logger.info(f"Excel report exported to {output_path}")
    print(f"Excel report saved to {output_path}")

export_to_excel()