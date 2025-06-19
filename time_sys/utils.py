from datetime import datetime, timedelta
from .models import TimeRecord
import pytz

def invertDictionary(d):
    myDict = {}
    for i in d:
        value = d.get(i)
        myDict.setdefault(value, []).append(i)
    return myDict

def timezone_display(user):
 # --- conver "+/-" in timezone into daily use format
    if user.timezone[7]=="-":
        timezone_string = user.timezone.replace("-", "+")
    else:
        timezone_string = user.timezone.replace("+", "-")
    return timezone_string
    # ---


def listToString(list):
    listToStr = ' '.join([str(elem) for elem in list])
    return listToStr


def month_jump(last_utc, this_utc):
    if this_utc.month > last_utc.month:
        next_month_start = datetime(this_utc.year, this_utc.month, 1, tzinfo=pytz.UTC)
        prev_month_end = next_month_start - timedelta(seconds=1)
        duration1 = prev_month_end - last_utc
        duration2 = this_utc - next_month_start
        result = {
            'end1': prev_month_end,
            'duration1': int(duration1.total_seconds()),
            'duration2': int(duration2.total_seconds()),
        }
        return result
    else:
        return False
