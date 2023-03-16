import requests

def call_url(url: str, timeout: int = 5) -> requests.Response:
    """
    Sends an HTTP GET request to the specified URL with the given timeout.

    Parameters:
        url (str): The URL to send the request to.
        timeout (int): The maximum number of seconds to wait for a response.

    Returns:
        requests.Response: A `Response` object containing information about the response from the server,
            or `None` if an error occurs.
    """
    response = None
    try:
        response = requests.get(url=url, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("Timeout error occurred")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
    finally:
        print("Request completed")
    return response