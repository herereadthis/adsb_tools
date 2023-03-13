from timezonefinder import TimezoneFinder

def get_timezone_name(latitude, longitude):
    """
    Gets the name of the timezone based on coordinates
    """
    tf = TimezoneFinder()
    timezone_name = tf.timezone_at(lat=latitude, lng=longitude)

    return timezone_name