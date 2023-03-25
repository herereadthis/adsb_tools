from adsb_tools.utils import requests_utils

class Receiver:
    def __init__(self, base_adsb_url):
        self.url = f'{base_adsb_url}/data/receiver.json'
        receiver = requests_utils.get_api(self.url)
        self.version = receiver['version']
        self.refresh = receiver['refresh']
        self.history = receiver['history']
        self.version = receiver['version']
        self.lat = receiver['lat']
        self.lon = receiver['lon']
        self.latitude = receiver['lat']
        self.longitude = receiver['lon']
