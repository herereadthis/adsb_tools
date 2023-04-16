from datetime import datetime
import pytz
from typing import Optional

def format_datetime(datetime_str, local_tz):
    if datetime_str is None:
        return None

    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
    # tz = pytz.timezone(timezone)
    # print(f'dt: {dt}')
    # print(f'tz: {tz}')
    
    # Create a timezone object for the UTC timezone
    utc_tz = pytz.timezone('UTC')
    
    # Make the datetime object timezone-aware with the UTC timezone
    datetime_obj_utc = utc_tz.localize(datetime_obj)
    
    # Convert the datetime object to the local timezone
    local_tz = pytz.timezone(local_tz)
    datetime_obj_local = datetime_obj_utc.astimezone(local_tz)
    
    # Format the datetime object as a string in the desired format
    formatted_datetime = datetime_obj_local.strftime('%a %d %b, %I:%M %p %Z')

    return formatted_datetime   

    # localized_dt = tz.localize(dt, is_dst=None)
    # formatted_dt = localized_dt.strftime('%d %b, %I:%M %p %Z')
    # return formatted_dt

def get_time_diff(dt_str2: Optional[str], dt_str1: Optional[str]) -> Optional[int]:
    dt_format = '%Y-%m-%dT%H:%M:%SZ'
    diff_in_minutes = None
    try:
        timestamp1 = datetime.strptime(dt_str1, dt_format)
        timestamp2 = datetime.strptime(dt_str2, dt_format)
        diff_in_minutes = round((timestamp2 - timestamp1).total_seconds() / 60, 2)
        diff_in_minutes = (timestamp2 - timestamp1).total_seconds() / 60
        if (diff_in_minutes < 10):
            diff_in_minutes = round(diff_in_minutes, 1)
        else:
            diff_in_minutes = round(diff_in_minutes)
    except ValueError:
        diff_in_minutes = None
    return diff_in_minutes
