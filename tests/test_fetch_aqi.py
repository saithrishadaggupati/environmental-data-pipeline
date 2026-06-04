import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ingestion.fetch_aqi import get_air_quality_label, CITIES

def test_label_boundary_moderate():
    assert get_air_quality_label(100) == "Moderate"

def test_label_boundary_unhealthy():
    assert get_air_quality_label(200) == "Unhealthy"

def test_all_cities_have_lat_lon():
    for city in CITIES:
        assert "lat" in city and "lon" in city, f"{city['name']} missing lat/lon"

def test_city_count():
    assert len(CITIES) == 101