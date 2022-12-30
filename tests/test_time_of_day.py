#!/usr/bin/env python3
from datetime import datetime

from garmin_activity_share.tweet import get_time_of_day


def test_get_time_of_day():
    """Test the get_time_of_day function with various times and timezones"""

    # Africa/Lusaka is UTC +2
    assert get_time_of_day(datetime(2022, 1, 1, 5, 0)) == "morning"
    assert get_time_of_day(datetime(2022, 9, 30, 10, 0), timezone="Africa/Lusaka") == "afternoon"
    assert get_time_of_day(datetime(2022, 4, 21, 16, 59), timezone="Africa/Lusaka") == "evening"

    # America/Chicago is UTC -6
    assert get_time_of_day(datetime(2022, 1, 1, 5, 0), timezone="America/Chicago") == "evening"
    assert get_time_of_day(datetime(2022, 9, 30, 10, 0), timezone="America/Chicago") == "morning"
    assert get_time_of_day(datetime(2022, 4, 21, 16, 59), timezone="America/Chicago") == "morning"

    # Pacific/Fiji is UTC +12
    assert get_time_of_day(datetime(2022, 1, 1, 5, 0), timezone="Pacific/Fiji") == "evening"
    assert get_time_of_day(datetime(2022, 9, 30, 10, 0), timezone="Pacific/Fiji") == "evening"
    assert get_time_of_day(datetime(2022, 4, 21, 16, 59), timezone="Pacific/Fiji") == "morning"
