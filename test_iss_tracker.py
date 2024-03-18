from iss_tracker import getLLA
from datetime import datetime
from astropy import coordinates
from astropy import units
import time
from iss_tracker import *
from datetime import datetime, timedelta


def test_calculate_speed():
    # Test the speed calculation with known values
    # This should result in a speed of 5 (3-4-5 triangle)
    x_dot, y_dot, z_dot = 4, 3, 0
    expected_speed = 5
    calculated_speed = calculate_speed(x_dot, y_dot, z_dot)
    assert calculated_speed == expected_speed


def test_convert_epoch_to_datetime():
    # Test the custom epoch to datetime conversion
    epoch = "2024-047T12:00:00.000Z"
    # Expected result based on the epoch string. Adjust this to match the expected datetime object.
    # Adjusted to the correct datetime for the example epoch
    expected_datetime = datetime(2024, 2, 16, 12, 0)
    converted_datetime = convert_epoch_to_datetime(epoch)

    # Assert that the converted datetime matches the expected datetime
    assert converted_datetime == expected_datetime


def test_getLLA():
    # Test the getLLA function with known values
    sv = {
        'X': {'#text': '407.811'},
        'Y': {'#text': '-4867.064'},
        'Z': {'#text': '4989.635'},
        'EPOCH': '2024-067T08:28:00.000Z'
    }
    expected_result = (45.7965, -11.323, 615.008)
    result = getLLA(sv)
    assert abs(result[0] - expected_result[0]) < 0.001
    assert abs(result[1] - expected_result[1]) < 0.001
    assert abs(result[2] - expected_result[2]) < 0.001


def test_getLLA_negative_coordinates():
    # Test the getLLA function with negative coordinates
    sv = {
        'X': {'#text': '-407.811'},
        'Y': {'#text': '4867.064'},
        'Z': {'#text': '-4989.635'},
        'EPOCH': '2024-067T08:28:00.000Z'
    }
    expected_result = (-45.796, 168.676, 615.008)
    result = getLLA(sv)
    assert abs(result[0] - expected_result[0]) < 0.001
    assert abs(result[1] - expected_result[1]) < 0.001
    assert abs(result[2] - expected_result[2]) < 0.001


def test_getLLA_different_units():
    # Test the getLLA function with different units
    sv = {
        'X': {'#text': '407811.0'},
        'Y': {'#text': '-4867064.0'},
        'Z': {'#text': '4989635.0'},
        'EPOCH': '2024-067T08:28:00.000Z'
    }
    expected_result = (45.6212, -11.323, 6975830.0846)
    result = getLLA(sv)

    assert abs(result[0] - expected_result[0]) < 0.001
    assert abs(result[1] - expected_result[1]) < 0.001
    assert abs(result[2] - expected_result[2]) < 0.001


def test_getLLA_different_epoch():
    # Test the getLLA function with different epoch
    sv = {
        'X': {'#text': '407.811'},
        'Y': {'#text': '-4867.064'},
        'Z': {'#text': '4989.635'},
        'EPOCH': '2024-068T08:28:00.000Z'
    }
    expected_result = (45.7965, -12.3090, 615.008)
    result = getLLA(sv)
    assert abs(result[0] - expected_result[0]) < 0.001
    assert abs(result[1] - expected_result[1]) < 0.001
    assert abs(result[2] - expected_result[2]) < 0.001


def test_getGeoLoc():
    # Test the getGeoLoc function with a valid latitude and longitude
    lat = 29.979
    lon = -95.336
    expected_result = "Houston"
    result = getGeoLoc(lat, lon)
    assert result["city"] == expected_result


def test_getGeoLoc_no_location():
    # Test the getGeoLoc function with invalid latitude and longitude
    lat = 0
    lon = 0
    expected_result = "No location data"
    result = getGeoLoc(lat, lon)
    assert result == expected_result
