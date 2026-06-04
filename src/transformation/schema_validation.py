from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional
import pandas as pd
from src.logger import logger


class AQIRecord(BaseModel):
    city: str
    aqi_index: float
    timestamp: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @field_validator("city")
    @classmethod
    def city_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("city name cannot be empty")
        return v.strip()

    @field_validator("aqi_index")
    @classmethod
    def aqi_must_be_in_range(cls, v):
        if v < 0 or v > 500:
            raise ValueError(f"aqi_index {v} is outside valid range 0–500")
        return v

    @field_validator("timestamp")
    @classmethod
    def timestamp_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("timestamp cannot be empty")
        return v


def validate_dataframe(df: pd.DataFrame) -> dict:
    valid_rows = []
    invalid_rows = []

    for _, row in df.iterrows():
        try:
            record = AQIRecord(
                city=str(row.get("city", "")),
                aqi_index=float(row.get("aqi_index", -1)),
                timestamp=str(row.get("timestamp", "")),
                latitude=row.get("latitude", None),
                longitude=row.get("longitude", None),
            )
            valid_rows.append(record.model_dump())
        except ValidationError as e:
            invalid_rows.append({
                "city": row.get("city", "unknown"),
                "errors": str(e)
            })

    logger.info(f"Schema validation complete — {len(valid_rows)} valid, {len(invalid_rows)} invalid")

    if invalid_rows:
        for r in invalid_rows:
            logger.warning(f"Invalid record [{r['city']}]: {r['errors']}")

    return {
        "valid_count": len(valid_rows),
        "invalid_count": len(invalid_rows),
        "valid_rows": valid_rows,
        "invalid_rows": invalid_rows,
    }


if __name__ == "__main__":
    import os
    if os.path.exists("data/raw/aqi_data.csv"):
        df = pd.read_csv("data/raw/aqi_data.csv")
        result = validate_dataframe(df)
        print(f"\nValid rows   : {result['valid_count']}")
        print(f"Invalid rows : {result['invalid_count']}")
        if result["invalid_rows"]:
            print("\nInvalid records:")
            for r in result["invalid_rows"]:
                print(f"  {r['city']}: {r['errors']}")
    else:
        logger.error("No data file found at data/raw/aqi_data.csv")