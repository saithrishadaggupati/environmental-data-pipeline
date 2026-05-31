import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.transformation.clean_aqi import label_air

def test_good_aqi():
    assert label_air(30) == "Good"

def test_moderate_aqi():
    assert label_air(80) == "Moderate"

def test_unhealthy_aqi():
    assert label_air(150) == "Unhealthy"

def test_hazardous_aqi():
    assert label_air(300) == "Hazardous"

def test_boundary_good():
    assert label_air(50) == "Good"