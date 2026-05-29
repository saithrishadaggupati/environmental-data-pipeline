import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cur = conn.cursor()

cur.execute("SELECT COUNT(*), COUNT(DISTINCT city) FROM aqi_readings")
total, cities = cur.fetchone()
print(f"Total records: {total}")
print(f"Total cities: {cities}")

cur.execute("SELECT air_quality_label, COUNT(*) FROM aqi_readings GROUP BY air_quality_label")
print("Labels breakdown:")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}")

conn.close()