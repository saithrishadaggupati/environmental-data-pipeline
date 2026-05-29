import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from src.logger import logger

load_dotenv()


def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )


def export_to_excel():
    logger.info("Starting Excel export")

    engine = get_engine()
    df = pd.read_sql("SELECT * FROM aqi_readings", engine)
    logger.info(f"Fetched {len(df)} rows from PostgreSQL")

    os.makedirs("data/exports", exist_ok=True)
    output_path = "data/exports/AQI_India_Report.xlsx"

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="AQI Data", index=False)

        summary = df.groupby("air_quality_label")["city"].count().reset_index()
        summary.columns = ["Air Quality Label", "City Count"]
        summary.to_excel(writer, sheet_name="Summary", index=False)

    logger.info(f"Excel report saved to {output_path}")


if __name__ == "__main__":
    export_to_excel()