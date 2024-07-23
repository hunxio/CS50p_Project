import pytest
from project import get_coordinates

# Testing get_coordinates if returns value when called
def test_NYCoordinates():
    assert get_coordinates("New York") == {"latitude": 40.7127281, "longitude": -74.0060152}

def test_LondonCoordinates():
    assert get_coordinates("London") == {"latitude": 51.5074456, "longitude": -0.1277653}

def test_BlankInput():
    assert get_coordinates("Rome") == {"latitude": 41.8933203, "longitude": 12.4829321}

    