import pytest
from project import get_coordinates

# Testing get_coordinates if returns value when called
def test_get_coordinates():
    assert get_coordinates("New York") == {"latitude": 40.7127281, "longitude": -74.0060152}


