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


