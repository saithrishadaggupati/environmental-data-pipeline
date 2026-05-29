import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aqi_readings (
            id                SERIAL PRIMARY KEY,
            city              VARCHAR(100) NOT NULL,
            aqi_index         NUMERIC(8, 2),
            pm2_5             NUMERIC(8, 2),
            pm10              NUMERIC(8, 2),
            co                NUMERIC(8, 2),
            air_quality_label VARCHAR(50),
            timestamp         TIMESTAMP,
            created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Table ready")

def load_data(csv_path):
    df = pd.read_csv(csv_path)
    conn = get_connection()
    cursor = conn.cursor()
    rows_inserted = 0
    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO aqi_readings 
                (city, aqi_index, pm2_5, pm10, co, air_quality_label, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                row['city'],
                row['aqi_index'],
                row['pm2_5'],
                row['pm10'],
                row['co'],
                row['air_quality_label'],
                row['timestamp']
            ))
            rows_inserted += 1
        except Exception as e:
            print(f"Skipped row: {e}")
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Inserted {rows_inserted} rows into PostgreSQL")

if __name__ == "__main__":
    create_table()
    load_data("data/processed/clean_aqi.csv")