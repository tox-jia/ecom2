from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from django.utils import timezone
import datetime

from store.models import Profile
from store.forms import UpdateUserForm
import pytz
# import json
#
from .models import TimeRecord, TimeTag, TimeReport
from .forms import TimeCheckoutForm, SettingsForm, DeleteTagForm, RecordDel
from .utils import timezone_display, month_jump


@login_required
@user_passes_test(lambda u: u.is_superuser)
def time_checkout(request):
    form = TimeCheckoutForm(request.POST or None)
    form_del = RecordDel(request.POST or None)
    tags = TimeTag.objects.all()
    record_qs = TimeRecord.objects.all()
    checkout_time = timezone.now()

    if not tags.exists():
        messages.error(request, 'Please create a Time-Tag first.')
        return redirect('time_settings')

    if not record_qs.exists():
        TimeRecord.objects.create(
            tag='start',
            end=checkout_time,  # <- this_utc, not datetime.this_utc()
            duration=0,
            type='UN'
        )
        messages.success(request, "Started first record.")
        return redirect('time_checkout')

    else:
        this_utc = timezone.now()
        last_utc = record_qs.order_by('-id').first().end

        if request.method == 'POST':
            form_type = request.POST.get("form_type")
            # ----------------------------------#
            # Checkout #
            # ------------ Start ---------------#
            if form_type=="checkout" and form.is_valid():
                tag_raw = form.cleaned_data['time_tag'].split("-", 2)
                time_switch = form.cleaned_data['time_switch']
                # ----------------------------------#
                # Switch is on #
                # ------------ Start ---------------#
                if time_switch:
                    this_raw = form.cleaned_data['time_correction']
                    if timezone.is_aware(this_raw):
                        this_naive = this_raw.replace(tzinfo=None)
                        # // strip off the timezone info by using replace(tzinfo=None)
                    else:
                        this_naive = this_raw

                    user_tz = pytz.timezone(request.user.profile.timezone)
                    this_local = user_tz.localize(this_naive)

                    this_utc = this_local.astimezone(pytz.UTC)

                    if this_utc <= last_utc or this_utc > timezone.now():
                        messages.error(request, "Invalid time.")
                        return redirect('time_checkout')

                    duration = this_utc - last_utc
                    checkout_time = this_utc
                # ----------------------------------#
                # Switch is off #
                # ------------ Start ---------------#
                else:
                    duration = this_utc - last_utc
                    checkout_time = this_utc
                # END ------------------------------#


                # ----------------------------------#
                # Month Jump #
                # // by using "utlis.py"
                # ------------ Start ---------------#
                month_jump_result = month_jump(last_utc, this_utc)
                if month_jump_result:
                    TimeRecord.objects.create(
                        tag=tag_raw[0],
                        end=month_jump_result['end1'],
                        duration=month_jump_result['duration1'],
                        type=tag_raw[1]
                    )
                    TimeRecord.objects.create(
                        tag=tag_raw[0],
                        end=checkout_time,
                        duration=month_jump_result['duration2'],
                        type=tag_raw[1]
                    )
                else:
                    TimeRecord.objects.create(
                        tag=tag_raw[0],
                        end=checkout_time,
                        duration=int(duration.total_seconds()),
                        type=tag_raw[1]
                    )
                # END ------------------------------#


                # messages.success(request, "Time checkout successfully.")
                return redirect('time_checkout')
            # END ------------------------------#


            # ----------------------------------#
            # Delete the record by clicking 'x' #
            # ----------------------------------#
            elif form_type=="del" and form_del.is_valid():
                record_del = TimeRecord.objects.filter(id=form_del.cleaned_data['del_id']).first()
                record_del.delete()
                return redirect('time_checkout')
            # END ------------------------------#


    if form.errors:
        for field, errs in form.errors.items():
            for err in errs:
                messages.error(request, f'{field}: {err}')

    records = TimeRecord.objects.order_by('-id')[:2]

    context = {
        'form': form,
        'form_del':form_del,
        'tags': tags,
        'timezone': timezone_display(request.user.profile),
        'now': this_utc,
        'last': last_utc if record_qs.exists() else None,
        'records': records
    }
    return render(request, 'time/time_checkout.html', context)










@login_required
@user_passes_test(lambda u: u.is_superuser)
def time_records(request):
    records = TimeRecord.objects.all().order_by('-id')
    form = RecordDel(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        record_del = TimeRecord.objects.filter(id=form.cleaned_data['del_id']).first()
        record_del.delete()
        messages.success(request, "Deleted")
    context = {
        'records': records,
        'timezone': timezone_display(request.user.profile),
    }
    return render(request, 'time/time_records.html', context)










@login_required
@user_passes_test(lambda u: u.is_superuser)
def time_report(request):
    from .utils import generate_monthly_report
    generate_monthly_report()  # Ensure new reports are created if needed

    reports = TimeReport.objects.all().order_by('-year_month')
    report_data = []

    for report in reports:
        if report.total_duration:
            tag_percent = {
                tag: [round(dur / 60) , round(dur / report.total_duration * 100, 2)]
                for tag, dur in report.tag_data.items()
            }
            type_percent = {
                typ: [round(dur / 60), round(dur / report.total_duration * 100, 2)]
                for typ, dur in report.type_data.items()
            }
        else:
            tag_percent = {}
            type_percent = {}

        report_data.append({
            'month': report.year_month,
            'total_duration': report.total_duration,
            'tag_percent': tag_percent,
            'type_percent': type_percent,
        })
        #// report_data is a list [...], Containing multiple dictionaries {...}
        #// Some values in those dictionaries (like tag_percent, type_percent) are nested dictionaries
        #// report_data = [
        #     {
        #         'month': '2025-06',
        #         'total_duration': 748491,
        #         'tag_percent': {
        #             'Nap': 95.24,
        #             'Studying': 4.64,
        #             'Eating': 0.0,
        #         },
        #         'type_percent': {
        #             'RS': 95.24,
        #             'PR': 4.7,
        #             'UN': 0.06,
        #         },
        #     },
        #     {
        #         'month': '2025-07',
        #         'total_duration': 746640,
        #         'tag_percent': {
        #             'Workout': 92.57,
        #             'Studying': 7.43,
        #         },
        #         'type_percent': {
        #             'PR': 100.0,
        #         },
        #     },
        #     ...
        # ]

    context = {
        'report_data': report_data,
        'timezone': timezone_display(request.user.profile),
    }
    return render(request, 'time/time_report.html', context)










@login_required
@user_passes_test(lambda u: u.is_superuser)
def time_settings(request):
    form1 = SettingsForm(request.POST or None)
    form2 = DeleteTagForm(request.POST or None)
    form3 = UpdateUserForm(request.POST or None, instance=request.user.profile)
    tags = TimeTag.objects.all()

    if not tags.exists():
        tag_data = [
            {"tag": "Sleep", "type": "RS"},
            {"tag": "Eating", "type": "UN"},
            {"tag": "Workout", "type": "PR"},
            {"tag": "Driving", "type": "UN"},
            {"tag": "Nap", "type": "RS"},
            {"tag": "Studying", "type": "PR"},
            {"tag": "Working", "type": "PR"},
            {"tag": "Shopping", "type": "UN"},
        ]

        for item in tag_data:
            TimeTag.objects.create(**item)

        tags = TimeTag.objects.all()

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "settings_form":
            if form1.is_valid():
                tag_to_create = TimeTag(
                    tag=form1.cleaned_data['setting_tag'],
                    type=form1.cleaned_data['setting_type'],
                )
                tag_to_create.save()
                messages.success(request, f"You created tag: {tag_to_create.tag}")
                return redirect('time_settings')

        elif form_type == "delete_tag_form":
            if form2.is_valid():
                selected_tag = tags.filter(tag=form2.cleaned_data['selecting_tag']).first()
                selected_tag.delete()
                messages.success(request, "Deleted")
                return redirect('time_settings')

        elif form_type == "change_timezone_form":
            if form3.is_valid():
                form3.save()
                messages.success(request, "Updated")
                return redirect('time_settings')

    context = {
        'form': form1,
        'form2': form2,
        'form3': form3,
        'tags': tags,
    }

    return render(request, 'time/time_settings.html', context)

