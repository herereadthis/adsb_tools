import math
import numbers
from adsb_tools.utils import requests_utils, spatial_utils, dt_utils, aeroapi_utils
from pprint import pprint

EARTH_RADIUS_KM = 6371.0

RADIUS_EARTH_FEET = 20925524.9  # Radius of the Earth in feet
RADIUS_EARTH_MILES = 3958.8  # Radius of the Earth in miles
RADIUS_EARTH_KM = 6371.0  # Radius of the Earth in kilometers
RADIUS_EARTH_NM = 3440.1  # Radius of the Earth in nautical miles
RADIUS_EARTH_METERS = 6371000.0  # Radius of the Earth in meters

class Aircraft:
    def __init__(self, base_adsb_url, base_latitude=None, base_longitude=None, flightaware_api_key=None):
        self.base_adsb_url = base_adsb_url
        self.earth_radius_km = EARTH_RADIUS_KM
        aircraft_list = self.get_aircraft_list()
        self.aircraft_list = aircraft_list
        self.nearest_aircraft = {}
        self.base_latitude = None
        self.base_longitude = None
        self.flightaware_api_key = flightaware_api_key
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
            flight_options = hex_db_options

        nearest_aircraft.update(flight_options)
        nearest_aircraft['image'] = aircraft_image
        nearest_aircraft['identity'] = {
            **flight_options,
            'image': aircraft_image
        }

        if ('flightaware_urls' in nearest_aircraft and bool(nearest_aircraft['flightaware_urls'])):
            live_url = f"https://flightaware.com/live/flight/{flight_options['registration']}"
            nearest_aircraft['flightaware_urls']['live'] = live_url

        self.nearest_aircraft = nearest_aircraft

    
    def set_flightaware_ident(self):
        headers = {'x-apikey': self.flightaware_api_key}
        nearest_aircraft = self.nearest_aircraft
        registration = nearest_aircraft['identity']['registration']

        aeroapi_url = f'https://aeroapi.flightaware.com/aeroapi/flights/{registration}'
        json_obj = requests_utils.get_api(url=aeroapi_url, headers=headers)

        current_flight = {}
        if ('flights' in json_obj and len(json_obj['flights']) != 0):
            flights = json_obj['flights']
            filtered_data = [d for d in flights if not d['status'].lower().startswith(('scheduled', 'arrived'))]
            current_flight = filtered_data[0] if len(filtered_data) > 0 else {}

            if ('scheduled_in' in current_flight and 'estimated_in' in current_flight
                and current_flight['scheduled_in']):
                current_flight['diff_arrival_minutes'] = aeroapi_utils.calculate_arrival_delay(current_flight)
                current_flight['diff_departure_minutes'] = aeroapi_utils.calculate_departure_delay(current_flight)
        
        if bool(current_flight):
            nearest_aircraft['flightaware'] = current_flight
        
        return current_flight


    def map_static_aircraft_options(self, stored_aircraft):
        """
        Maps static aircraft information from a stored aircraft dictionary to the nearest aircraft dictionary.
        """
        keys_to_map = [
            'identity',
            'flightaware',
            'flightaware_urls'
        ]
        for key in keys_to_map:
            if key in stored_aircraft:
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

                distances = spatial_utils.calculate_distances(
                    self.base_latitude, self.base_longitude, aircraft_lat, aircraft_lon
                )
                degrees = spatial_utils.get_degrees(
                    self.base_latitude, self.base_longitude, aircraft_lat, aircraft_lon
                )
                direction = spatial_utils.get_cardinal_direction(degrees)

                new_aircraft['distance'] = {
                    **distances,
                    'degrees': degrees,
                    'direction': direction,
                }
                new_aircraft['icao_24'] = aircraft['hex']
                movement = {}
                if ('track' in aircraft and isinstance(aircraft['track'], numbers.Number)):
                    movement = {
                        'track': aircraft['track'],
                        'direction': spatial_utils.get_cardinal_direction(aircraft['track'])
                    }
                new_aircraft['movement'] = movement

                mode_s = aircraft['hex']
                redirect_url = f"https://flightaware.com/live/modes/{mode_s}/redirect"
                if ('flight' in aircraft and bool(aircraft['flight'])):
                    redirect_url = f"https://flightaware.com/live/modes/{mode_s}/ident/{aircraft['flight']}/redirect"

                new_aircraft['flightaware_urls'] = {
                    'redirect': redirect_url
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
        response = adsb_db_obj['response']

        result = {}
        if (type(response) is dict and 'aircraft' in response):
            adsb_aircraft = response['aircraft']
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
            result = requests_utils.map_keys(adsb_aircraft, mapped_keys)
        return result
    

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
        with_distance_sorted = sorted(with_distance, key=lambda x: x.get("distance").get("km", float("inf")))

        # Combine the two lists, with dictionaries with distance at the beginning
        return with_distance_sorted + without_distance
