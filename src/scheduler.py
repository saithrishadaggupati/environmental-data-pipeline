import schedule
import time
import subprocess
import sys
from datetime import datetime

def run_pipeline():
    print(f"\n🔄 Pipeline started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1 - Fetch fresh AQI data
    print("📡 Step 1: Fetching AQI data...")
    subprocess.run([sys.executable, "src/ingestion/fetch_aqi.py"])
    
    # Step 2 - Clean the data
    print("🧹 Step 2: Cleaning data...")
    subprocess.run([sys.executable, "src/transformation/clean_aqi.py"])
    
    # Step 3 - Load into PostgreSQL
    print("🗄️ Step 3: Loading into PostgreSQL...")
    subprocess.run([sys.executable, "src/loading/load_to_postgres.py"])
    
    print(f"✅ Pipeline complete at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("⏰ Next run in 6 hours\n")

# Run once immediately on startup
run_pipeline()

# Then repeat every 6 hours
schedule.every(6).hours.do(run_pipeline)

print("🔁 Scheduler running... Press Ctrl+C to stop")

while True:
    schedule.run_pending()
    time.sleep(60)