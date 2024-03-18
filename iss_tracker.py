from math import sqrt
import requests
import xmltodict
from datetime import datetime, timedelta
import logging
import time
from astropy import coordinates
from astropy import units
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
    return sqrt(x_dot**2 + y_dot**2 + z_dot**2)


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
        # Convert target_datetime to offset-aware datetime
        target_datetime = target_datetime.replace(tzinfo=epoch_datetime.tzinfo)
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
    """
    Fetches the state vectors of the International Space Station (ISS).

    Returns:
        list: A list of state vectors representing the position and velocity of the ISS.
    """
    state_vectors = fetch_iss_data()
    return state_vectors['ndm']['oem']['body']['segment']['data']['stateVector']


def getLLA(sv):
    """
    Convert satellite coordinates from Cartesian to latitude, longitude, and altitude.

    Parameters:
    - sv (dict): A dictionary containing satellite coordinates in Cartesian format.

    Returns:
    - tuple: A tuple containing latitude, longitude, and altitude values.
    """
    x = float(sv['X']['#text'])
    y = float(sv['Y']['#text'])
    z = float(sv['Z']['#text'])

    # assumes epoch is in format '2024-067T08:28:00.000Z'
    this_epoch = time.strftime(
        '%Y-%m-%d %H:%m:%S', time.strptime(sv['EPOCH'][:-5], '%Y-%jT%H:%M:%S'))

    cartrep = coordinates.CartesianRepresentation([x, y, z], unit=units.km)
    gcrs = coordinates.GCRS(cartrep, obstime=this_epoch)
    itrs = gcrs.transform_to(coordinates.ITRS(obstime=this_epoch))
    loc = coordinates.EarthLocation(*itrs.cartesian.xyz)

    return loc.lat.value, loc.lon.value, loc.height.value


def getGeoLoc(lat, lon):
    """
    Retrieves the address information for a given latitude and longitude.

    Parameters:
        lat (float): The latitude coordinate.
        lon (float): The longitude coordinate.

    Returns:
        str: The address information as a string, or "No location data" if no location is found.
    """
    geolocator = Nominatim(user_agent="iss-tracker")
    location = geolocator.reverse(f"{lat}, {lon}", language='en', zoom=15)
    return location.raw["address"] if location else "No location data"


def main():

    pass


if __name__ == "__main__":
    main()
