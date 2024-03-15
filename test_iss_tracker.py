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


