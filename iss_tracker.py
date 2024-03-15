import math
import requests
import xmltodict
from datetime import datetime, timedelta
import time
from math import *
import logging
from typing import List, Dict, Optional
from geopy.geocoders import Nominatim

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_iss_data() -> Optional[List[Dict]]:
    """
    Fetches ISS trajectory data from the specified URL and parses it into a list of dictionaries.

    Parameters:
        url (str): The URL from which to fetch the ISS data.

    Returns:
        Optional[List[Dict]]: A list of state vectors if data fetch and parse are successful, None otherwise.
    """
    url = "https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml"
    try:
        response = requests.get(url)
        data = xmltodict.parse(response.content)
        return data
    except Exception as e:
        logging.error(f"Error fetching or parsing ISS data: {e}")
        return None


def calculate_speed(x_dot: float, y_dot: float, z_dot: float) -> float:
    """
    Calculates the speed of the ISS given its velocity components.

    Parameters:
        x_dot (float): The velocity of the ISS along the X-axis.
        y_dot (float): The velocity of the ISS along the Y-axis.
        z_dot (float): The velocity of the ISS along the Z-axis.

    Returns:
        float: The calculated speed of the ISS.
    """
    return math.sqrt(x_dot**2 + y_dot**2 + z_dot**2)


def find_closest_epoch(state_vectors: List[Dict], target_datetime: datetime) -> Dict:
    """
    Finds the state vector closest to the specified target datetime.

    Parameters:
        state_vectors (List[Dict]): A list of ISS state vectors.
        target_datetime (datetime): The target datetime to find the closest state vector to.

    Returns:
        Dict: The state vector closest to the target datetime.
    """
    closest_time = None
    closest_sv = None
    for sv in state_vectors:
        epoch_datetime = convert_epoch_to_datetime(sv['EPOCH'])
        if closest_time is None or abs(epoch_datetime - target_datetime) < abs(closest_time - target_datetime):
            closest_time = epoch_datetime
            closest_sv = sv
    return closest_sv


def convert_epoch_to_datetime(epoch: str) -> datetime:
    """
    Converts an epoch string into a datetime object.

    Parameters:
        epoch (str): The epoch string to convert.

    Returns:
        datetime: The converted datetime object.
    """
    year_str, rest = epoch.split('-')
    year = int(year_str)
    doy_str, time_str = rest.split('T')
    doy = int(doy_str)  

    time_parts = time_str.replace('Z', '').split(':')
    hours, minutes = int(time_parts[0]), int(time_parts[1])
    seconds = float(time_parts[2])

    date = datetime(year, 1, 1) + timedelta(days=doy - 1,
                                            hours=hours, minutes=minutes, seconds=seconds)

    return date


def get_epochs():
    state_vectors = fetch_iss_data()
    return state_vectors['ndm']['oem']['body']['segment']['data']['stateVector']

def main():
    """
    Main function to execute the ISS tracking script.
    """
    
    pass


if __name__ == "__main__":
    main()
