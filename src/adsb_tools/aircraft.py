import math
from adsb_tools.utils import requests_utils
# from pprint import pprint

EARTH_RADIUS_KM = 6371.0

class Aircraft:
    def __init__(self, base_adsb_url, base_latitude=None, base_longitude=None):
        self.base_adsb_url = base_adsb_url
        self.earth_radius_km = EARTH_RADIUS_KM
        aircraft_list = self.get_aircraft_list()
        self.aircraft_list = aircraft_list
        self.nearest_aircraft = {}
        self.base_latitude = None
        self.base_longitude = None
        if (base_latitude and base_longitude):
            self.base_latitude = base_latitude
            self.base_longitude = base_longitude
            self.augment_aircraft_list()
            self.set_nearest_aircraft()


    def augment_aircraft_list(self):
        """
        Adds additional options to the aircraft list and sets it as the new `aircraft_list`.
        This method does not exist as part of init, so that it can be called separately by whatever has instantiated the
        Aircraft class
        """
        aircraft_list = self.add_aircraft_options()
        self.aircraft_list = aircraft_list


    def set_nearest_aircraft(self):
        """
        Sets the nearest aircraft to the current location and adds links to various databases.

        The function creates a copy of the first aircraft in the aircraft list, adds links to the HEXDB and ADSB databases,
        and sets the result as the nearest aircraft.

        Returns:
            None
        """
        # dict creates a copy of the dictionary. aircraft_list remains unaffected.
        nearest_aircraft = dict(self.aircraft_list[0])
        icao_24 = nearest_aircraft['hex']
        nearest_aircraft['hexdb'] = {
            'aircraft_url': f'https://hexdb.io/api/v1/aircraft/{icao_24}',
            'conversion_url': f'https://hexdb.io/hex-reg?hex={icao_24}'
        }
        nearest_aircraft['adsb_db'] = {
            'aircraft_url': f'https://api.adsbdb.com/v0/aircraft/{icao_24}',
            'conversion_url': f'https://api.adsbdb.com/v0/mode-s/{icao_24}'
        }

        self.nearest_aircraft = nearest_aircraft


    def retrieve_external_aircraft_options(self):
        """
        Retrieves external flight information and aircraft image for the nearest aircraft.
        Then updates the `nearest_aircraft` dictionary with the aircraft image URL and the merged flight information.
        """
        nearest_aircraft = self.nearest_aircraft
        icao_24 = nearest_aircraft['icao_24']
        aircraft_image = Aircraft.get_aircraft_image(icao_24)
        hex_db_options = Aircraft.get_hex_db_flight(icao_24)
        adsb_db_options = Aircraft.get_adsb_db_flight(icao_24)

        flight_options = {}
        if adsb_db_options:
            flight_options = adsb_db_options
        elif hex_db_options:
            flight_options= hex_db_options

        nearest_aircraft.update(flight_options)
        nearest_aircraft['image'] = aircraft_image

        if ('flightaware' in nearest_aircraft and bool(nearest_aircraft['flightaware'])):
            live_url = f"https://flightaware.com/live/flight/{flight_options['registration']}"
            nearest_aircraft['flightaware']['live_url'] = live_url

        self.nearest_aircraft = nearest_aircraft


    def map_static_aircraft_options(self, stored_aircraft):
        """
        Maps static aircraft information from a stored aircraft dictionary to the nearest aircraft dictionary.
        """
        keys_to_map = [
            'country_iso',
            'country_name',
            'icao_type_code',
            'manufacturer',
            'mode_s',
            'operator_flag_code',
            'owner',
            'registration',
            'type',
            'image',
            'flightaware'
        ]
        for key in keys_to_map:
            self.nearest_aircraft[key] = stored_aircraft[key]


    def get_aircraft_list(self):
        """
        Get the aircraft messages and returns as list
        """
        aircraft_url = f'{self.base_adsb_url}/data/aircraft.json'
        json_obj = requests_utils.get_api(aircraft_url)
        result = json_obj['aircraft']

        return result


    def add_aircraft_options(self):
        """
        Adds additional data to aircraft based on aircraft properties
        """
        aircraft_list_with_options = []
        for aircraft in self.aircraft_list:
            if 'flight' in aircraft:
                aircraft['flight'] = aircraft['flight'].strip()
            if Aircraft.get_has_coordinates(aircraft):
                new_aircraft = aircraft.copy()
                aircraft_lat = new_aircraft['lat']
                aircraft_lon = new_aircraft['lon']

                distance = Aircraft.calculate_distance(
                    self.base_latitude, self.base_longitude, aircraft_lat, aircraft_lon
                )
                degrees, direction = Aircraft.get_direction(
                    self.base_latitude, self.base_longitude, aircraft_lat, aircraft_lon
                )

                new_aircraft['distance'] = distance
                new_aircraft['degrees'] = degrees
                new_aircraft['direction'] = direction
                new_aircraft['icao_24'] = aircraft['hex']

                mode_s = aircraft['hex']
                redirect_url = f"https://flightaware.com/live/modes/{mode_s}/redirect"
                if ('flight' in aircraft and bool(aircraft['flight'])):
                    redirect_url = f"https://flightaware.com/live/modes/{mode_s}/ident/{aircraft['flight']}/redirect"

                new_aircraft['flightaware'] = {
                    'redirect_url': redirect_url
                }

                aircraft_list_with_options.append(new_aircraft)
            else:
                aircraft_list_with_options.append(aircraft)

        return Aircraft.sort_by_distance(aircraft_list_with_options)


    @staticmethod
    def get_hex_db_flight(icao_24):
        """
        Get values from HexDB
        """
        hex_db_url = f'https://hexdb.io/api/v1/aircraft/{icao_24}'
        hex_db_obj = requests_utils.get_api(hex_db_url)

        mapped_keys = {
            'icao_type_code': 'ICAOTypeCode',
            'country_iso': None,
            'country_name': None,
            'manufacturer': 'Manufacturer',
            'mode_s': 'ModeS',
            'operator_flag_code': 'OperatorFlagCode',
            'owner': 'RegisteredOwners',
            'registration': 'Registration',
            'type': 'Type'
        }

        return requests_utils.map_keys(hex_db_obj, mapped_keys)


    @staticmethod
    def get_adsb_db_flight(icao_24):
        """
        Get values from ADSB DB
        """
        adsb_db_url = f'https://api.adsbdb.com/v0/aircraft/{icao_24}'
        adsb_db_obj = requests_utils.get_api(adsb_db_url)
        adsb_aircraft = adsb_db_obj['response']['aircraft']

        mapped_keys = {
            'icao_type_code': 'icao_type',
            'manufacturer': 'manufacturer',
            'country_iso': 'registered_owner_country_iso_name',
            'country_name': 'registered_owner_country_name',
            'mode_s': 'mode_s',
            'operator_flag_code': 'registered_owner_operator_flag_code',
            'owner': 'registered_owner',
            'registration': 'registration',
            'type': 'type'
        }

        return requests_utils.map_keys(adsb_aircraft, mapped_keys)
    

    @staticmethod
    def get_has_coordinates(aircraft = {}) -> bool:
        """
        Determine whether an aircraft has coordinates
        """
        return True if aircraft.get("lat") is not None and aircraft.get("lon") is not None else False


    @staticmethod
    def get_aircraft_image(aircraft_hex):
        """
        Gets the image of an aircraft, given its hex. If no image found, return
        empty dictionary.
        """
        headers = {
            'User-Agent': 'My Unique User Agent'
        }
        planespotter_url = f'https://api.planespotters.net/pub/photos/hex/{aircraft_hex}'
        json_obj = requests_utils.get_api(planespotter_url, headers = headers)

        image = {}
        if (json_obj['photos'] and json_obj['photos'][0] and bool(json_obj['photos'][0])):
            photo_attributes = json_obj['photos'][0]
            thumbnail = photo_attributes['thumbnail']
            thumbnail_large = photo_attributes['thumbnail_large']
            target_photo = thumbnail if thumbnail_large is None else thumbnail_large
            image = {
                'height': target_photo['size']['height'],
                'width': target_photo['size']['width'],
                'src': target_photo['src'],
                'url': planespotter_url
            }

        return image

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
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
        distance = EARTH_RADIUS_KM * angular_distance

        return distance


    @staticmethod
    def get_direction(base_lat, base_lon, dest_lat, dest_lon):
        """Calculate the direction from one coordinate to another."""
        # Calculate the difference between the latitudes and longitudes
        lat_diff = dest_lat - base_lat
        lon_diff = dest_lon - base_lon

        # Calculate the angle between the two points in radians
        angle = math.atan2(lon_diff, lat_diff)

        # Convert the angle from radians to degrees
        degrees = math.degrees(angle)

        # Convert the angle to a compass direction
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        idx = round(degrees / (360.0 / len(directions))) % len(directions)
        direction = directions[idx]

        return degrees, direction
    

    @staticmethod
    def sort_by_distance(data):
        """
        Sort a list of dictionaries based on their "distance" values, with dictionaries that have a defined
        "distance" value appearing first.
        """
        # Split dictionaries into those with a distance key and those without
        with_distance = []
        without_distance = []
        for d in data:
            if "distance" in d:
                with_distance.append(d)
            else:
                without_distance.append(d)

        # Sort dictionaries with distance by their distance values
        with_distance_sorted = sorted(with_distance, key=lambda x: x.get("distance", float("inf")))

        # Combine the two lists, with dictionaries with distance at the beginning
        return with_distance_sorted + without_distance
