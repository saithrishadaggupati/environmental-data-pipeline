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

def run_analysis():
    conn = get_connection()

    # Query 1 — Which cities have the worst air quality?
    print("\n🏙️ Top 5 Most Polluted Cities:")
    df1 = pd.read_sql("""
        SELECT city, aqi_index, air_quality_label
        FROM aqi_readings
        ORDER BY aqi_index DESC
        LIMIT 5
    """, conn)
    print(df1.to_string(index=False))

    # Query 2 — Average AQI by pollution category
    print("\n📊 Average AQI by Category:")
    df2 = pd.read_sql("""
        SELECT air_quality_label,
               COUNT(*) as total_cities,
               ROUND(AVG(aqi_index)::numeric, 2) as avg_aqi
        FROM aqi_readings
        GROUP BY air_quality_label
        ORDER BY avg_aqi DESC
    """, conn)
    print(df2.to_string(index=False))

    # Query 3 — Cities with AQI above national danger threshold
    print("\n⚠️ Cities Above Danger Threshold (AQI > 200):")
    df3 = pd.read_sql("""
        SELECT city, aqi_index, air_quality_label
        FROM aqi_readings
        WHERE aqi_index > 200
        ORDER BY aqi_index DESC
    """, conn)
    print(df3.to_string(index=False))

    # Query 4 — Clean vs polluted city ratio
    print("\n✅ Clean vs Polluted City Breakdown:")
    df4 = pd.read_sql("""
        SELECT 
            CASE 
                WHEN air_quality_label = 'Good' THEN 'Clean'
                ELSE 'Polluted'
            END as status,
            COUNT(*) as cities,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as percentage
        FROM aqi_readings
        GROUP BY status
    """, conn)
    print(df4.to_string(index=False))

    conn.close()

if __name__ == "__main__":
    run_analysis()