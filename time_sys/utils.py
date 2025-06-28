from datetime import datetime, timedelta
from .models import TimeRecord, TimeReport
from django.utils import timezone
from collections import defaultdict
import pytz


import re
def parse_duration_to_seconds(duration_str):
    # Pattern looks for groups like: 1h, 19m, 14s
    pattern = r'(?:(\d+)h)?\s*(?:(\d+)m)?\s*(?:(\d+)s)?'
    match = re.match(pattern, duration_str.strip())

    if not match:
        return 0

    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0

    return hours * 3600 + minutes * 60 + seconds


def timezone_display(user):
 # --- convert "+/-" in timezone into daily use format
    if user.timezone[7]=="-":
        timezone_string = user.timezone.replace("-", "+")
    else:
        timezone_string = user.timezone.replace("+", "-")
    return timezone_string



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




def generate_monthly_report(k):
    from django.db.models.functions import TruncMonth
    from django.db.models import Sum

    now = timezone.now()
    current_month_str = now.strftime("%Y-%m")

    all_months = (
        TimeRecord.objects.filter(user=k).annotate(month=TruncMonth("end"))
        #// annotate(), is to add a new field
        #// TruncMonth("end") takes the end datetime and truncates it to the first day of the month at 00:00.
        #// eg: end = 2025-06-23 14:45:00, TruncMonth("end"): 2025-06-01 00:00:00.
        .values_list("month", flat=True)
        #// This pulls out just the month values from the queryset.
		#// flat=True gives you a flat list like: [datetime(2025, 6, 1, 0, 0), datetime(2025, 7, 1, 0, 0), ...]
        .distinct()
        #// Removes duplicate months from the list, so you only get one entry per unique month.
    )

    for month_start in sorted(all_months):
        #// sort will put the data into ascending sequence:
        #// from [2025, 7, 1][2025, 10, 1][2025, 3, 1]
        #// to   [2025, 3, 1][2025, 7, 1][2025, 10, 1]
        #// Descending: sorted(all_months, reverse=True)
        if not month_start:
            continue
            #// continue means to skip this data and go for the next data in FOR loop.
            #// and the rest of the code won't be executed.

        year_month = month_start.strftime("%Y-%m")
        #// put the format into yyyy-mm, from "2025, 6, 1, 0, 0":" to "2025-6"
        if year_month < current_month_str:
            continue  # Skip only past months, not current or future

        next_month = (month_start + timedelta(days=32)).replace(day=1)
        #// 1. month_start + timedelta(days=32):
        #// Adds 32 days to month_start, no matter how long the current month is (28, 30, or 31 days),
        #// the result is in the next month
        #// 2. replace(day=1):
        #// Replaces the day of that new date with 1, i.e., sets it to the first day of that month.
        records = TimeRecord.objects.filter(user=k, end__gte=month_start, end__lt=next_month)
        #// Get all time_records from this month only.
        #// end__gte(gte = “greater than or equal”), end__lt= (less than)

        total_duration = sum(r.duration for r in records)
        #// very special and shrunk way to write code, shorter, cleaner, faster(no creating intermediate list)

        tag_data = defaultdict(int)
        type_data = defaultdict(int)
        #// is "from collections import defaultdict", a special dictionary type from Python’s collections module.
        #// with a built-in default value of 0 when a key is missing.
        #// eg: d = defaultdict(int)  |    d['a'] += 1    |    d['b'] += 3

        for r in records:
            tag_data[r.tag] += r.duration
            type_data[r.type] += r.duration

        TimeReport.objects.update_or_create(
            user=k,
            #// user=k passes an int (user ID), but user is a ForeignKey, so Django expects a **User instance`, not an int.
            year_month=year_month,
            #// is a hidden "if statement"
            #// it is equal to:
            # try:
            #     report = TimeReport.objects.get(year_month=year_month)
            #     # If found: UPDATE the fields
            #     report.total_duration = total_duration
            #     report.tag_data = dict(tag_data)
            #     report.type_data = dict(type_data)
            #     report.save()
            # except TimeReport.DoesNotExist:
            #     # If not found: CREATE a new record
            #     TimeReport.objects.create(
            #         year_month=year_month,
            #         total_duration=total_duration,
            #         tag_data=dict(tag_data),
            #         type_data=dict(type_data),
            #     )
            defaults={
                "total_duration": total_duration,
                "tag_data": dict(tag_data),
                "type_data": dict(type_data),
            }
        )