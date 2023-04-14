import datetime
import pytz

def format_datetime(datetime_str, local_tz):
    if datetime_str is None:
        return None

    datetime_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
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
    formatted_datetime = datetime_obj_local.strftime('%d %b, %I:%M %p %Z')

    return formatted_datetime   

    # localized_dt = tz.localize(dt, is_dst=None)
    # formatted_dt = localized_dt.strftime('%d %b, %I:%M %p %Z')
    # return formatted_dt

def get_time_diffs(dt_str1, dt_str2):
    dt_format = '%Y-%m-%dT%H:%M:%SZ'
    diff_in_minutes = None
    try:
        timestamp1 = datetime.datetime.strptime(dt_str1, dt_format)
        timestamp2 = datetime.datetime.strptime(dt_str2, dt_format)
        diff_in_minutes = round((timestamp2 - timestamp1).total_seconds() / 60, 2)
    except ValueError:
        diff_in_minutes = None
    return diff_in_minutes
