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