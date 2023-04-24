from datetime import datetime
import pytz
from typing import Optional

DT_FORMAT_READABLE = '%a %d %b, %I:%M %p %Z'
DT_FORMAT_DEFAULT = '%Y-%m-%dT%H:%M:%SZ'

def format_datetime(datetime_str, local_tz, conversion=DT_FORMAT_READABLE, format=DT_FORMAT_DEFAULT):
    if datetime_str is None:
        return None

    datetime_obj = datetime.strptime(datetime_str, format)
    # tz = pytz.timezone(timezone)
    
    # Create a timezone object for the UTC timezone
    utc_tz = pytz.timezone('UTC')
    
    # Make the datetime object timezone-aware with the UTC timezone
    datetime_obj_utc = utc_tz.localize(datetime_obj)
    
    # Convert the datetime object to the local timezone
    local_tz = pytz.timezone(local_tz)
    datetime_obj_local = datetime_obj_utc.astimezone(local_tz)
    
    # Format the datetime object as a string in the desired format
    formatted_datetime = datetime_obj_local.strftime(conversion)

    return formatted_datetime   

    # localized_dt = tz.localize(dt, is_dst=None)
    # formatted_dt = localized_dt.strftime('%d %b, %I:%M %p %Z')
    # return formatted_dt

def format_date_short(datetime_str, local_tz):
    return format_datetime(datetime_str, local_tz, '%a, %d %B')

def format_time_short(datetime_str, local_tz):
    return format_datetime(datetime_str, local_tz, '%H:%M')

def format_tz(datetime_str, local_tz):
    return format_datetime(datetime_str, local_tz, '%Z')


def compare_datetimes(date1, date2, format=DT_FORMAT_DEFAULT):
    try:
        dt1 = datetime.strptime(date1, format)
        dt2 = datetime.strptime(date2, format)
        if dt1 > dt2:
            return 1
        elif dt1 < dt2:
            return -1
        else:
            return 0
    except ValueError:
        return 0


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
    except TypeError:
        diff_in_minutes = None
    return diff_in_minutes
