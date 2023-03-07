from typing import List, Dict
import math

EARTH_RADIUS_KM = 6371.0


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculates the great-circle distance between two points on the Earth's surface
    using the Haversine formula.

    Args:
        lat1 (float): Latitude of the first point in degrees
        lon1 (float): Longitude of the first point in degrees
        lat2 (float): Latitude of the second point in degrees
        lon2 (float): Longitude of the second point in degrees

    Returns:
        float: Distance between the two points in kilometers
    """

    # Convert coordinates to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = EARTH_RADIUS_KM * c

    return distance


def find_closest(
        coordinates: List[Dict[str, float]],
        target_lat: float,
        target_lon: float
        ) -> Dict[str, float]:
    """
    Finds the dictionary in `coordinates` that is closest to the given target 
    coordinates.

    Args:
        coordinates (List[Dict[str, float]]): A list of dictionaries where each
                dictionary has 'latitude' and 'longitude' keys containing float
                values.
        target_lat (float): Target latitude in degrees
        target_lon (float): Target longitude in degrees

    Returns:
        Dict[str, float]: The dictionary in `coordinates` that is closest to the
                target coordinates.
    """

    closest_dict = None
    closest_distance = float('inf')

    for coordinate in coordinates:
        lat = coordinate['latitude']
        lon = coordinate['longitude']
        distance = calculate_distance(lat, lon, target_lat, target_lon)

        if distance < closest_distance:
            closest_dict = coordinate
            closest_distance = distance

    return closest_dict
