import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from src.logger import logger

load_dotenv()


def store_raw_to_mongo():
    logger.info("Connecting to MongoDB Atlas")
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["aqi_database"]
    collection = db["raw_readings"]

    df = pd.read_csv("data/raw/aqi_data.csv")
    records = df.to_dict("records")

    for record in records:
        record["ingested_at"] = datetime.utcnow()

    result = collection.insert_many(records)
    logger.info(f"Inserted {len(result.inserted_ids)} records into MongoDB")

    client.close()
    logger.info("MongoDB connection closed")
    return len(result.inserted_ids)


if __name__ == "__main__":
    store_raw_to_mongo()