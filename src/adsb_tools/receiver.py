import json
import requests

def get_receiver(base_url):
    receiver_url = f'{base_url}/data/receiver.json'

    response = requests.get(receiver_url)
    json_obj = json.loads(response.content)

    return json_obj
