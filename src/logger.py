import logging
import os
from datetime import datetime

# Create logs folder if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Log file name includes today's date
log_filename = f"logs/pipeline_{datetime.now().strftime('%Y-%m-%d')}.log"

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        # Write to file
        logging.FileHandler(log_filename),
        # Also print to terminal
        logging.StreamHandler()
    ]
)

# Create logger object
logger = logging.getLogger("aqi_pipeline")