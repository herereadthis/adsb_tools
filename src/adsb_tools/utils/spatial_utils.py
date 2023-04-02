"""
Spatial Utilities
"""

import math
import numbers

RADIUS_EARTH_FEET = 20925524.9  # Radius of the Earth in feet
RADIUS_EARTH_MILES = 3958.8  # Radius of the Earth in miles
RADIUS_EARTH_KM = 6371.0  # Radius of the Earth in kilometers
RADIUS_EARTH_NM = 3440.1  # Radius of the Earth in nautical miles
RADIUS_EARTH_METERS = 6371000.0  # Radius of the Earth in meters


def calculate_distances(lat1, lon1, lat2, lon2):
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
    square_half_chord = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    angular_distance = 2 * math.atan2(math.sqrt(square_half_chord), math.sqrt(1-square_half_chord))

    # return distance
    return {
        "ft": RADIUS_EARTH_FEET * angular_distance,
        "mi": RADIUS_EARTH_MILES * angular_distance,
        "km": RADIUS_EARTH_KM * angular_distance,
        "nm": RADIUS_EARTH_NM * angular_distance,
        "m": RADIUS_EARTH_METERS * angular_distance
    }



def get_degrees(base_lat, base_lon, dest_lat, dest_lon):
    """Calculate the degrees from one coordinate to another."""
    # Calculate the difference between the latitudes and longitudes
    lat_diff = dest_lat - base_lat
    lon_diff = dest_lon - base_lon

    # Calculate the angle between the two points in radians
    angle = math.atan2(lon_diff, lat_diff)

    # Convert the angle from radians to degrees
    return math.degrees(angle)


def get_cardinal_direction(degrees):
    """Calculate the direction from one coordinate to another."""
    # Convert the angle to a compass direction
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    idx = round(degrees / (360.0 / len(directions))) % len(directions)
    return directions[idx]
