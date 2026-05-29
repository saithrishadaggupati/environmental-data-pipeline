import pandas as pd

def run_quality_checks(df):
    """
    Runs data quality checks on AQI data.
    Prints a report and returns cleaned data.
    """
    print("\n📋 Running data quality checks...")
    
    total = len(df)
    issues = 0

    # Check 1 — Missing city names
    missing_cities = df['city'].isnull().sum()
    if missing_cities > 0:
        print(f"  ⚠️ {missing_cities} rows have missing city names")
        df = df.dropna(subset=['city'])
        issues += missing_cities
    else:
        print(f"  ✅ No missing city names")

    # Check 2 — Invalid AQI values
    invalid_aqi = df[df['aqi_index'] < 0].shape[0]
    if invalid_aqi > 0:
        print(f"  ⚠️ {invalid_aqi} rows have negative AQI values")
        df = df[df['aqi_index'] >= 0]
        issues += invalid_aqi
    else:
        print(f"  ✅ All AQI values are valid")

    # Check 3 — Duplicate cities
    duplicates = df.duplicated(subset=['city']).sum()
    if duplicates > 0:
        print(f"  ⚠️ {duplicates} duplicate city entries found")
        df = df.drop_duplicates(subset=['city'])
        issues += duplicates
    else:
        print(f"  ✅ No duplicate cities")

    # Check 4 — Missing AQI values
    missing_aqi = df['aqi_index'].isnull().sum()
    if missing_aqi > 0:
        print(f"  ⚠️ {missing_aqi} rows have missing AQI values")
        df = df.dropna(subset=['aqi_index'])
        issues += missing_aqi
    else:
        print(f"  ✅ No missing AQI values")

    print(f"\n📊 Quality Report:")
    print(f"  Total records checked: {total}")
    print(f"  Issues found and fixed: {issues}")
    print(f"  Clean records: {len(df)}")
    
    return df

if __name__ == "__main__":
    df = pd.read_csv("data/processed/clean_aqi.csv")
    df = run_quality_checks(df)