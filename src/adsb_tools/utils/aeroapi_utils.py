from typing import Dict, Optional
from adsb_tools.utils import dt_utils

def get_first_value(values):
    nums = [x for x in values if isinstance(x, (int, float)) and x is not None]
    return nums[0] if nums else None


def calculate_arrival_delay(flightaware: Dict[str, Optional[str]]) -> Optional[int]:
    scheduled_in = flightaware.get('scheduled_in')
    estimated_in = flightaware.get('estimated_in')
    scheduled_on = flightaware.get('scheduled_on')
    estimated_on = flightaware.get('estimated_on')
    
    time_diff_0 = dt_utils.get_time_diff(estimated_in, scheduled_in)
    time_diff_1 = dt_utils.get_time_diff(estimated_on, scheduled_on)
    time_diff_2 = dt_utils.get_time_diff(estimated_in, scheduled_on)
    time_diff_3 = dt_utils.get_time_diff(estimated_on, scheduled_in)

    time_diffs = [
        time_diff_0, time_diff_1, time_diff_2, time_diff_3
    ]

    return get_first_value(time_diffs)

def calculate_departure_delay(flightaware: Dict[str, Optional[str]]) -> Optional[int]:
    scheduled_out = flightaware.get('scheduled_out')
    estimated_out = flightaware.get('estimated_out')
    actual_out = flightaware.get('actual_out')
    scheduled_off = flightaware.get('scheduled_off')
    estimated_off = flightaware.get('estimated_off')
    actual_off = flightaware.get('actual_off')
    
    time_diff_0 = dt_utils.get_time_diff(actual_out, scheduled_out)
    time_diff_1 = dt_utils.get_time_diff(actual_out, scheduled_off)
    time_diff_2 = dt_utils.get_time_diff(actual_off, scheduled_out)
    time_diff_3 = dt_utils.get_time_diff(actual_off, scheduled_off)
    time_diff_4 = dt_utils.get_time_diff(estimated_out, scheduled_out)
    time_diff_5 = dt_utils.get_time_diff(estimated_out, scheduled_off)
    time_diff_6 = dt_utils.get_time_diff(estimated_off, scheduled_out)
    time_diff_7 = dt_utils.get_time_diff(estimated_off, scheduled_off)

    time_diffs = [
        time_diff_0, time_diff_1, time_diff_2, time_diff_3, time_diff_4, time_diff_5, time_diff_6, time_diff_7
    ]

    return get_first_value(time_diffs)