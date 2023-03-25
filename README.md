# adsb_tools

Scripts and stuff to help you parse through data from [Dump1090] messages. 

Dump1090 is a Mode S decoder specifically designed for RTLSDR devices. It is a simple ADS-B (Automatic Dependent 
Surveillance - Broadcast) receiver, decoder and web-server. It requires a RTLSDR USB-stick and Osmocom's librtlsdr.
FlightAware maintains the [current version of Dump1090](https://github.com/flightaware/dump1090).


## Aircraft Class

```python
from adsb_tools.aircraft import Aircraft
"""
You must provide the base url for your ADS-B feeder,
E.g., localhost:8080 or 192.x.x.x:8080
Optional: provide base_latitude and base_longitude, which can be the
coordinates of your receiver. By providing base coordinates, each aircraft 
message will be augmented with additional info, including distance from base
coordinates, and direction. Nearest aircraft will be identified, and additional
external info will be retrieved, e.g. registration, image
"""
aircraft = Aircraft(base_adsb_url, base_latitude, base_longitude)
# get nearest aircraft
nearest_aircraft = aircraft.nearest_aircraft
```


This class has methods to augment and provide additional information about aircrafts based on ADS-B messages. The class takes in ADS-B messages from Dump1090 aircraft JSON and a base station's coordinates (latitude and longitude) as input. The class then calculates the distance and direction of each aircraft from the base station and adds this information to the ADS-B messages.

The class has the following methods:

* `__init__(self, base_adsb_url, base_latitude=None, base_longitude=None)`: The class constructor. It initializes the base_adsb_url, earth_radius_km, aircraft_list, and nearest_aircraft properties. If the base_latitude and base_longitude arguments are provided, the augment_aircraft_list() and set_nearest_aircraft() methods are called.
* `augment_aircraft_list(self)`: This method adds additional options to the aircraft list based on aircraft properties. The new options include the aircraft's distance from the base station, the direction of the aircraft from the base station, and the aircraft's ICAO 24-bit address.
* `set_nearest_aircraft(self)`: This method finds the nearest aircraft to the base station and adds links to various databases, such as the HEXDB and ADSB databases.
* `retrieve_external_aircraft_options(self)`: This method retrieves external flight information and aircraft images for the nearest aircraft. It updates the nearest_aircraft dictionary with the aircraft image URL and the merged flight information.
* `map_static_aircraft_options(self, stored_aircraft)`: This method maps static aircraft information from a stored aircraft dictionary to the nearest aircraft dictionary.
* `get_aircraft_list(self)`: This method retrieves the aircraft messages and returns them as a list.
* `add_aircraft_options(self)`: This method adds additional data to aircraft based on aircraft properties. It calculates the distance and direction of each aircraft from the base station and adds this information to the aircraft message. It also adds the aircraft's ICAO 24-bit address to the message.
