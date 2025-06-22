from datetime import datetime, timedelta
from .models import TimeRecord, TimeReport
from django.utils import timezone
from collections import defaultdict
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




def generate_monthly_report():
    from django.db.models.functions import TruncMonth
    from django.db.models import Sum

    now = timezone.now()
    current_month_str = now.strftime("%Y-%m")

    all_months = (
        TimeRecord.objects.annotate(month=TruncMonth("end"))
        .values_list("month", flat=True)
        .distinct()
    )

    for month_start in sorted(all_months):
        if not month_start:
            continue

        year_month = month_start.strftime("%Y-%m")
        if year_month < current_month_str:
            continue  # ✅ Skip only past months, not current or future

        next_month = (month_start + timedelta(days=32)).replace(day=1)
        records = TimeRecord.objects.filter(end__gte=month_start, end__lt=next_month)

        total_duration = sum(r.duration for r in records)
        tag_data = defaultdict(int)
        type_data = defaultdict(int)

        for r in records:
            tag_data[r.tag] += r.duration
            type_data[r.type] += r.duration

        TimeReport.objects.update_or_create(
            year_month=year_month,
            defaults={
                "total_duration": total_duration,
                "tag_data": dict(tag_data),
                "type_data": dict(type_data),
            }
        )
