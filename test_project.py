import pytest
from project import get_coordinates, validation

# Testing get_coordinates if returns value when called
def test_new_york_coordinates():
    assert get_coordinates("New York") == {"latitude": 40.7127281, "longitude": -74.0060152}

def test_london_coordinates():
    assert get_coordinates("London") == {"latitude": 51.5074456, "longitude": -0.1277653}

def test_rome_coordinates():
    assert get_coordinates("Rome") == {"latitude": 41.8933203, "longitude": 12.4829321}

