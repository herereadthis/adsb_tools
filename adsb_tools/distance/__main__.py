from .calculate import find_closest


if __name__ == '__main__':
    # Example usage
    coordinates = [
        {'latitude': 37.7749, 'longitude': -122.4194},
        {'latitude': 51.5074, 'longitude': -0.1278},
        {'latitude': 35.6895, 'longitude': 139.6917},
        {'latitude': -33.8651, 'longitude': 151.2094}
    ]

    target_lat = 40.7128
    target_lon = -74.0060

    closest_dict = find_closest(coordinates, target_lat, target_lon)

    print(f"The closest dictionary is: {closest_dict}")
