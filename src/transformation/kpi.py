import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from src.logger import logger

load_dotenv()


def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
        connect_args={"sslmode": "require"}
    )


def run_kpis():
    logger.info("Running KPI analysis on PostgreSQL")
    engine = get_engine()

    kpis = {
        # KPI 1 — National AQI average
        "national_avg_aqi": """
            SELECT ROUND(AVG(aqi_index), 2) AS national_avg_aqi
            FROM aqi_readings
        """,

        # KPI 2 — % of cities in each category
        "category_distribution": """
            SELECT air_quality_label,
                   COUNT(*) AS city_count,
                   ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct
            FROM aqi_readings
            GROUP BY air_quality_label
            ORDER BY city_count DESC
        """,

        # KPI 3 — Top 10 most polluted cities
        "top_polluted": """
            SELECT city, aqi_index, air_quality_label
            FROM aqi_readings
            ORDER BY aqi_index DESC
            LIMIT 10
        """,

        # KPI 4 — Cities exceeding WHO safe limit (AQI > 100)
        "unsafe_cities": """
            SELECT COUNT(*) AS unsafe_city_count,
                   ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM aqi_readings), 1) AS pct_unsafe
            FROM aqi_readings
            WHERE aqi_index > 100
        """,

        # KPI 5 — City health score (inverse of AQI, normalised 0-100)
        "city_health_scores": """
            SELECT city,
                   aqi_index,
                   ROUND(100.0 - (aqi_index * 100.0 / (SELECT MAX(aqi_index) FROM aqi_readings)), 1)
                       AS health_score
            FROM aqi_readings
            ORDER BY health_score DESC
            LIMIT 10
        """,

        # KPI 6 — Pollution gap: worst vs best city
        "pollution_gap": """
            SELECT MAX(aqi_index) AS worst_aqi,
                   MIN(aqi_index) AS best_aqi,
                   MAX(aqi_index) - MIN(aqi_index) AS pollution_gap
            FROM aqi_readings
        """,

        # KPI 7 — Cities at hazardous level
        "hazardous_cities": """
            SELECT city, aqi_index
            FROM aqi_readings
            WHERE aqi_index > 200
            ORDER BY aqi_index DESC
        """,

        # KPI 8 — Average AQI trend from history (last 5 runs)
        "aqi_trend": """
            SELECT timestamp,
                   ROUND(AVG(aqi_index), 2) AS avg_aqi
            FROM aqi_history
            GROUP BY timestamp
            ORDER BY timestamp DESC
            LIMIT 5
        """,
    }

    results = {}
    with engine.connect() as conn:
        for name, query in kpis.items():
            try:
                df = pd.read_sql(text(query), conn)
                results[name] = df
            except Exception as e:
                logger.warning(f"KPI {name} failed: {e}")

    print("\n=== AQI KPI Report ===\n")
    for name, df in results.items():
        print(f"--- {name.replace('_', ' ').title()} ---")
        print(df.to_string(index=False))
        print()

    logger.info("KPI analysis complete")
    return results


if __name__ == "__main__":
    run_kpis()