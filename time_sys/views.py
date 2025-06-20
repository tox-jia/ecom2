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
    tags = TimeTag.objects.all()
    record_qs = TimeRecord.objects.all()
    checkout_time = timezone.now()

    if not tags.exists():
        messages.error(request, 'Please create a Time-Tag first.')
        return redirect('time_settings')

    if record_qs.exists():
        this_utc = timezone.now()
        last_utc = record_qs.order_by('-id').first().end

        if request.method == 'POST' and form.is_valid():
            time_switch = form.cleaned_data['time_switch']

            if time_switch:
                this_raw = form.cleaned_data['time_correction']
                if timezone.is_aware(this_raw):
                    this_naive = this_raw.replace(tzinfo=None)
                    #// strip off the timezone info by using replace(tzinfo=None)
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
            else:
                duration = this_utc - last_utc
                checkout_time = this_utc

            tag_raw = form.cleaned_data['time_tag'].split("-", 2)
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
                # ----------------------------------#
                # End #
                # ------------ Start ---------------#
            # messages.success(request, "Time checkout successfully.")
            return redirect('time_checkout')

    else:
        TimeRecord.objects.create(
            tag='start',
            end=checkout_time,  # <- this_utc, not datetime.this_utc()
            duration=0,
            type='UN'
        )
        messages.success(request, "Started first record.")
        return redirect('time_checkout')

    if form.errors:
        for field, errs in form.errors.items():
            for err in errs:
                messages.error(request, f'{field}: {err}')

    records = TimeRecord.objects.order_by('-id')[:1]

    context = {
        'form': form,
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
    return render(request, 'time/time_report.html', {})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def time_settings(request):
    form1 = SettingsForm(request.POST or None)
    form2 = DeleteTagForm(request.POST or None)
    form3 = UpdateUserForm(request.POST or None, instance=request.user.profile)
    tags = TimeTag.objects.all()

    if not tags.exists():
        tag_data = [
            {"tag": "Sleep", "type": "SL"},
            {"tag": "Eating", "type": "UN"},
            {"tag": "Workout", "type": "PR"},
            {"tag": "Driving", "type": "UN"},
            {"tag": "Nap", "type": "SL"},
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

