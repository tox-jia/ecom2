from datetime import datetime, timedelta
from .models import TimeRecord, TimeReport
from django.utils import timezone
from collections import defaultdict
import pytz
import math


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





def get_or_create_time_report(user, current_ym):
    report = TimeReport.objects.filter(user=user, year_month=current_ym).first()
    if not report:
        report = TimeReport.objects.create(
            user=user,
            year_month=current_ym,
            total_duration=0,
            type_data={},
            tag_data={},
            day_pr_data={}
        )
    return report





def generate_monthly_report(k,first_checkout_dic):
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
                "day_pr_data": dict(first_checkout_dic),
            }
        )



def generate_wheel(n, length, thickness1, thickness2):
    angle_deg = 360/n/2
    angle_rad = math.radians(angle_deg)
    angle_rad2 = 2*math.radians(angle_deg)
    tri_o = [0, 0]
    tri_a = [length, 0]
    tri_b = [length*math.cos(angle_rad2), length*math.sin(angle_rad2)]

    tri_o1 = [thickness1/math.tan(angle_rad), thickness1]
    inner_length = length - thickness1 / math.tan(angle_rad) - thickness1 * math.tan(angle_rad) - thickness2 / math.cos(angle_rad)
    tri_a1 = [thickness1 / math.tan(angle_rad) + inner_length, thickness1]
    tri_b1 = [
        thickness1 / math.tan(angle_rad) + inner_length * math.cos(angle_rad2),
        thickness1 + inner_length * math.sin(angle_rad2)
    ]

    n_set = {}

    for f in range(n):
        rotation_angle = math.radians(360 / n * f)

        n_set['tri{}'.format(f)] = [
            angle_rotate(rotation_angle,tri_o),
            angle_rotate(rotation_angle,tri_a),
            angle_rotate(rotation_angle,tri_b)
        ]

        n_set['tri_s{}'.format(f)] = [
            angle_rotate(rotation_angle, tri_o1),
            angle_rotate(rotation_angle, tri_a1),
            angle_rotate(rotation_angle, tri_b1)
        ]

    return n_set


def generate_wheel_with_rotation(n, length, thickness1, thickness2, pr_tags):
    wheel = generate_wheel(n, length, thickness1, thickness2)
    result = []
    angle_per = 360 / n

    # Only for the main triangles (e.g., those with keys like "tri0", "tri1", etc.)
    for i in range(n):
        tri = wheel.get(f'tri_s{i}')
        angle = i * angle_per + angle_per / 2
        result.append({'points': tri,
                       'angle': angle,
                       'pr_tags': pr_tags[i],
                       'id': i+1,
                       })

    return result



def angle_rotate(angle_rad, point):
    x, y = point
    x_new = round(x * math.cos(angle_rad) - y * math.sin(angle_rad))
    y_new = round(x * math.sin(angle_rad) + y * math.cos(angle_rad))
    return [x_new, y_new]
