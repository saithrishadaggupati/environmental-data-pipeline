import pandas as pd
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from src.logger import logger

load_dotenv()


def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )


def ensure_table(engine):
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS aqi_readings (
                city TEXT PRIMARY KEY,
                aqi_index INTEGER,
                pm2_5 FLOAT,
                pm10 FLOAT,
                co FLOAT,
                air_quality_label TEXT,
                timestamp TEXT
            )
        """))
        conn.commit()
    logger.info("Table aqi_readings is ready")


def load_data(csv_path="data/processed/clean_aqi.csv"):
    logger.info(f"Loading data from {csv_path} into PostgreSQL")
    df = pd.read_csv(csv_path)
    logger.info(f"Found {len(df)} rows to load")

    engine = get_engine()
    ensure_table(engine)

    with engine.connect() as conn:
        for _, row in df.iterrows():
            conn.execute(text("""
                INSERT INTO aqi_readings 
                    (city, aqi_index, pm2_5, pm10, co, air_quality_label, timestamp)
                VALUES 
                    (:city, :aqi_index, :pm2_5, :pm10, :co, :air_quality_label, :timestamp)
                ON CONFLICT (city) DO UPDATE SET
                    aqi_index = EXCLUDED.aqi_index,
                    pm2_5 = EXCLUDED.pm2_5,
                    pm10 = EXCLUDED.pm10,
                    co = EXCLUDED.co,
                    air_quality_label = EXCLUDED.air_quality_label,
                    timestamp = EXCLUDED.timestamp
            """), row.to_dict())
        conn.commit()

    logger.info(f"Load complete — {len(df)} rows upserted")
    return df


if __name__ == "__main__":
    load_data()