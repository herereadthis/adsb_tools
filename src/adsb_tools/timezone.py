"""
This module provides a function to retrieve the name of the timezone for a given set of coordinates.

The function `get_timezone_name` uses the TimezoneFinder library to determine the timezone
at a specific latitude and longitude coordinate pair. It returns the name of the timezone as a string.

Example Usage:
--------------
>>> get_timezone_name(37.7749, -122.4194)
'America/Los_Angeles'
"""

from timezonefinder import TimezoneFinder

def get_timezone_name(latitude, longitude):
    """
    Gets the name of the timezone based on coordinates
    """
    tf = TimezoneFinder()
    timezone_name = tf.timezone_at(lat=latitude, lng=longitude)

    return timezone_name
