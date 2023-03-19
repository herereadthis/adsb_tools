import json
import requests
import time

def call_url(url: str, timeout: int = 5, headers: dict = {}) -> requests.Response:
    """
    Sends an HTTP GET request to the specified URL with the given timeout.

    Parameters:
        url (str): The URL to send the request to.
        timeout (int): The maximum number of seconds to wait for a response.

    Returns:
        requests.Response: A `Response` object containing information about the response from the server,
            or `None` if an error occurs.
    """
    start_time = time.time() * 1000
    try:
        print(f"{url}: attempting request...")
        response = requests.get(url=url, timeout=timeout, headers=headers)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print(f"{url}: timeout error occurred.")
    except requests.exceptions.HTTPError as err:
        print(f"{url}: HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"{url}: An error occurred: {err}")
    finally:
        end_time = time.time() * 1000
        print(f'{url}: request completed, {end_time - start_time:.0f}ms')
    return response


def get_api(url, timeout = 5, headers = {}):
    """
    makes a GET request to a Rest API and returns a dictionary or list
    """
    result = call_url(url, timeout, headers)
    content = json.loads(result.content)
    return content


def map_keys(original_dict, mapped_keys):
    """
    Takes the values from one dictionary and returns a new dictionary with the
    same values, but with different key names
    """
    new_dict = {}

    for key in mapped_keys:
        mapped_key = mapped_keys[key]
        if (mapped_key is None):
            new_dict[key] = None
        elif (mapped_key in original_dict):
            new_dict[key] = original_dict[mapped_key]

    return new_dict