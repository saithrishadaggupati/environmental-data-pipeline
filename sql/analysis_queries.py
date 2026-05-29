import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv
from src.logger import logger

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
    logger.info("Starting SQL analysis on AQI dataset")
    conn = get_connection()

    # Query 1 — Top 5 most polluted cities
    logger.info("Running Query 1 — Most polluted cities")
    df1 = pd.read_sql("""
        SELECT city, aqi_index, air_quality_label
        FROM aqi_readings
        ORDER BY aqi_index DESC
        LIMIT 5
    """, conn)
    print("\n🏙️ Top 5 Most Polluted Cities:")
    print(df1.to_string(index=False))

    # Query 2 — Average AQI by pollution category
    logger.info("Running Query 2 — Average AQI by category")
    df2 = pd.read_sql("""
        SELECT air_quality_label,
               COUNT(*) as total_cities,
               ROUND(AVG(aqi_index)::numeric, 2) as avg_aqi
        FROM aqi_readings
        GROUP BY air_quality_label
        ORDER BY avg_aqi DESC
    """, conn)
    print("\n📊 Average AQI by Category:")
    print(df2.to_string(index=False))

    # Query 3 — Cities above danger threshold
    logger.info("Running Query 3 — Cities above danger threshold")
    df3 = pd.read_sql("""
        SELECT city, aqi_index, air_quality_label
        FROM aqi_readings
        WHERE aqi_index > 200
        ORDER BY aqi_index DESC
    """, conn)
    print("\n⚠️ Cities Above Danger Threshold (AQI > 200):")
    print(df3.to_string(index=False))

    # Query 4 — Clean vs polluted ratio using window function
    logger.info("Running Query 4 — Clean vs polluted city ratio")
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
    print("\n✅ Clean vs Polluted City Breakdown:")
    print(df4.to_string(index=False))

    # Query 5 — City rankings using window function
    logger.info("Running Query 5 — City pollution rankings")
    df5 = pd.read_sql("""
        SELECT 
            city,
            aqi_index,
            air_quality_label,
            RANK() OVER (ORDER BY aqi_index DESC) as pollution_rank,
            ROUND(AVG(aqi_index) OVER(), 2) as national_avg
        FROM aqi_readings
        ORDER BY pollution_rank
    """, conn)
    print("\n🏆 City Pollution Rankings vs National Average:")
    print(df5.to_string(index=False))

    # Query 6 — CTE for high risk cities analysis
    logger.info("Running Query 6 — High risk city analysis using CTE")
    df6 = pd.read_sql("""
        WITH city_risk AS (
            SELECT 
                city,
                aqi_index,
                air_quality_label,
                CASE 
                    WHEN aqi_index > 200 THEN 'High Risk'
                    WHEN aqi_index > 100 THEN 'Moderate Risk'
                    ELSE 'Low Risk'
                END as risk_level
            FROM aqi_readings
        )
        SELECT 
            risk_level,
            COUNT(*) as total_cities,
            ROUND(AVG(aqi_index)::numeric, 2) as avg_aqi,
            MIN(city) as example_city
        FROM city_risk
        GROUP BY risk_level
        ORDER BY avg_aqi DESC
    """, conn)
    print("\n🔴 Risk Level Distribution