import json
import math
from adsb_tools.utils import requests_utils

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
        aircraft_list = self.add_aircraft_options()
        self.aircraft_list = aircraft_list
    

    def set_nearest_aircraft(self):
        # dict creates a copy of the dictionary. aircraft_list remains unaffected.
        nearest_aircraft = dict(self.aircraft_list[0])
        icao_24 = nearest_aircraft['icao']
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
        nearest_aircraft = self.nearest_aircraft
        icao_24 = nearest_aircraft['icao_24']
        aircraft_image = Aircraft.get_aircraft_image(icao_24)
        hex_db_options = Aircraft.get_hex_db_flight(icao_24)
        adsb_db_options = Aircraft.get_adsb_db_flight(icao_24)

        flight_options = {}
        if (adsb_db_options):
            flight_options = adsb_db_options
        elif (hex_db_options):
            flight_options= hex_db_options

        nearest_aircraft.update(flight_options)
        nearest_aircraft['image'] = aircraft_image

        if ('flightaware' in nearest_aircraft and bool(nearest_aircraft['flightaware'])):
            nearest_aircraft['flightaware']['live_url'] = f"https://flightaware.com/live/flight/{flight_options['registration']}"

        self.nearest_aircraft = nearest_aircraft

    
    def map_static_aircraft_options(self, stored_aircraft):
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


    def get_aircraft_list(self, filter_aircraft = True):
        """
        Get the aircraft messages and returns as list
        """
        aircraft_url = f'{self.base_adsb_url}/data/aircraft.json'

        response = requests_utils.call_url(aircraft_url)
        # response = requests.get(aircraft_url)
        json_obj = json.loads(response.content)
        result = json_obj

        if (filter_aircraft):
            result = [
                d for d in json_obj['aircraft']
                if "lat" in d and "lon" in d and d["lat"] is not None and d["lon"] is not None
            ]

        return result
    

    def add_aircraft_options(self):
        """
        Adds additional data to aircraft based on aircraft properties
        """
        aircraft_list_with_options = []
        for aircraft in self.aircraft_list:
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
            new_aircraft['icao'] = aircraft['hex']
            new_aircraft['icao_24'] = aircraft['hex']

            redirect_url = f"https://flightaware.com/live/modes/{aircraft['hex']}/redirect"
            if ('flight' in aircraft and bool(aircraft['flight'])):
                redirect_url = f"https://flightaware.com/live/modes/{aircraft['hex']}/ident/{aircraft['flight']}/redirect"

            new_aircraft['flightaware'] = {
                'redirect_url': redirect_url
            }

            aircraft_list_with_options.append(new_aircraft)

        return sorted(aircraft_list_with_options, key=lambda x: x["distance"])


    @staticmethod
    def get_hex_db_flight(icao_24):
        """
        Get values from HexDB
        """
        hex_db_url = f'https://hexdb.io/api/v1/aircraft/{icao_24}'
        hex_db_result = requests_utils.call_url(hex_db_url)
        # hex_db_result = requests.get(hex_db_url)
        hex_db_obj = json.loads(hex_db_result.content)

        return {
            'icao_type_code': hex_db_obj['ICAOTypeCode'],
            'country_iso': None,
            'country_name': None,
            'manufacturer': hex_db_obj['Manufacturer'],
            'mode_s': hex_db_obj['ModeS'],
            'operator_flag_code': hex_db_obj['OperatorFlagCode'],
            'owner': hex_db_obj['RegisteredOwners'],
            'registration': hex_db_obj['Registration'],
            'type': hex_db_obj['Type']
        }


    @staticmethod
    def get_adsb_db_flight(icao_24):
        """
        Get values from ADSB DB
        """
        adsb_db_url = f'https://api.adsbdb.com/v0/aircraft/{icao_24}'
        adsb_db_result = requests_utils.call_url(adsb_db_url)
        # adsb_db_result = requests.get(adsb_db_url)
        adsb_db_obj = json.loads(adsb_db_result.content)
        adsb_aircraft = adsb_db_obj['response']['aircraft']

        return {
            'icao_type_code': adsb_aircraft['icao_type'],
            'manufacturer': adsb_aircraft['manufacturer'],
            'country_iso': adsb_aircraft['registered_owner_country_iso_name'],
            'country_name': adsb_aircraft['registered_owner_country_name'],
            'mode_s': adsb_aircraft['mode_s'],
            'operator_flag_code': adsb_aircraft['registered_owner_operator_flag_code'],
            'owner': adsb_aircraft['registered_owner'],
            'registration': adsb_aircraft['registration'],
            'type': adsb_aircraft['type']
        }


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
        response = requests_utils.call_url(planespotter_url, headers=headers)
        # response = requests.get(planespotter_url, headers=headers)
        json_obj = json.loads(response.content)

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
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = EARTH_RADIUS_KM * c

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
