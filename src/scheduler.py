import schedule
import time
import subprocess
import sys

def run_pipeline():
    print("\n🔄 Pipeline started...")
    subprocess.run([sys.executable, "src/ingestion/fetch_aqi.py"])
    print("✅ Pipeline complete! Next run in 1 hour.\n")

# Run once immediately
run_pipeline()

# Repeat every hour
schedule.every(1).hours.do(run_pipeline)

print("⏰ Scheduler running... Press Ctrl+C to stop")

while True:
    schedule.run_pending()
    time.sleep(60)