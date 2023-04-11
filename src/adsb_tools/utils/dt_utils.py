import datetime
import pytz

def format_datetime(datetime_str, timezone):
    dt = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
    tz = pytz.timezone(timezone)
    localized_dt = tz.localize(dt, is_dst=None)
    formatted_dt = localized_dt.strftime('%d %b, %I:%M %p %Z')
    return formatted_dt
