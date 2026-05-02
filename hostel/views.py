from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Guest, Term, RoomState, MonthlyJob, MonthlyJobRecord, MonthlyJobImage
from .forms import CheckinForm

from django.http import JsonResponse
import json
from django.utils import timezone


# --------------------
# LANGUAGE PAGE
# --------------------
def language(request):
    if request.GET.get('reset'):
        request.session.flush()
    return render(request, 'hostel/language.html')


# --------------------
# CHECK-IN
# --------------------
def checkin(request):
    lang = request.GET.get('lang')

    if lang:
        request.session['lang'] = lang

    if 'lang' not in request.session:
        return redirect('language')

    lang = request.session.get('lang')

    if request.method == "POST":
        form = CheckinForm(request.POST, request.FILES)
        if form.is_valid():
            guest = form.save()
            request.session['guest_id'] = guest.id
            request.session['answers'] = {}
            return redirect('terms', step=1)
    else:
        form = CheckinForm()

    return render(request, 'hostel/checkin.html', {
        'form': form,
        'lang': lang
    })


# --------------------
# TERMS
# --------------------
def terms(request, step):
    if 'lang' not in request.session:
        return redirect('language')

    guest_id = request.session.get('guest_id')
    if not guest_id:
        return redirect('checkin')

    terms_list = list(Term.objects.all().order_by('id'))
    total = len(terms_list)

    if step > total:
        return redirect('summary')

    term = terms_list[step - 1]
    lang = request.session.get('lang')

    if request.method == "POST":
        answer = request.POST.get('answer')

        if answer != term.correct_answer:
            msg = term.get_warning(lang) or "Invalid answer"
            messages.error(request, msg)
            return redirect('terms', step=step)

        answers = request.session.get('answers', {})
        answers[str(term.id)] = answer
        request.session['answers'] = answers

        if step < total:
            return redirect('terms', step=step + 1)
        else:
            return redirect('summary')

    question = term.get_question(lang)

    return render(request, "hostel/terms.html", {
        "term": term,
        "question": question,
        "step": step,
        "total": total,
        "lang": lang,
    })


# --------------------
# SUMMARY
# --------------------
def summary(request):
    if 'lang' not in request.session:
        return redirect('language')

    guest_id = request.session.get('guest_id')
    if not guest_id:
        return redirect('checkin')

    guest = Guest.objects.get(id=guest_id)
    answers = request.session.get('answers', {})

    guest.terms_answers = answers
    guest.save()

    terms = Term.objects.all().order_by('id')
    lang = request.session.get('lang')

    return render(request, 'hostel/summary.html', {
        'guest': guest,
        'answers': answers,
        'terms': terms,
        'lang': lang
    })


# --------------------
# ACCESS PASSWORDS
# --------------------
ACCESS_PASSWORDS = {
    "clean": "1228",
    "glist": "1228",
    "monthly_job": "2024",
}

def access_gate(request):
    next_url = request.GET.get('next', '/')

    ROUTE_MAP = {
        "/hostel/clean/": "clean",
        "/hostel/glist/": "glist",
        "/hostel/monthly_job/": "monthly_job",
    }

    key = ROUTE_MAP.get(next_url)
    print("NEXT:", next_url)
    print("KEY:", key)

    if request.method == "POST":
        password = request.POST.get("password")

        if key and ACCESS_PASSWORDS.get(key) == password:
            request.session[f'access_{key}'] = True
            return redirect(next_url)
        else:
            return render(request, "access.html", {
                "error": "Wrong password",
                "next": next_url
            })

    return render(request, "access.html", {"next": next_url})


# --------------------
# GUEST LIST
# --------------------
def gList(request):
    if not request.session.get('access_glist'):
        return redirect("/hostel/access/?next=/hostel/glist/")

    guests = Guest.objects.all().order_by('-id')
    rooms = RoomState.objects.all().order_by('id')

    return render(request, 'hostel/glist.html', {
        'guest': guests,
        'rooms': rooms
    })


def assign_room(request, guest_id):
    if request.method == "POST":
        guest = get_object_or_404(Guest, id=guest_id)
        room_id = request.POST.get("room_id")

        if room_id:
            room = RoomState.objects.get(id=room_id)
            guest.room = room
            room_name = room.name
        else:
            guest.room = None
            room_name = None

        guest.save()

        return JsonResponse({
            "success": True,
            "room_name": room_name
        })

    return JsonResponse({"success": False})


# --------------------
# CLEAN
# --------------------
def clean(request):
    if not request.session.get('access_clean'):
        return redirect("/hostel/access/?next=/hostel/clean/")

    rooms = RoomState.objects.all().order_by('id')

    return render(request, 'hostel/clean.html', {
        'rooms1': rooms[:8],
        'rooms2': rooms[8:20],
        'rooms3': rooms[20:],
    })


def update_room(request):
    data = json.loads(request.body)
    room = RoomState.objects.get(id=data.get("id"))
    field = data.get("field")

    if field == "out":
        room.out = not room.out
        room.is_extend = False
    elif field == "extend":
        room.is_extend = True
        room.out = False
    elif field == "off":
        room.out = False
        room.is_extend = False
        room.key = False
        room.is_clean = False
    elif field == "key":
        room.key = not room.key
    elif field == "clean":
        room.is_clean = not room.is_clean

    room.save()
    return JsonResponse({"status": "ok"})


def reset_rooms(request):
    if request.method == "POST":
        RoomState.objects.update(
            out=False,
            key=False,
            is_clean=False,
            is_extend=False,
        )
        return JsonResponse({"status": "ok"})

    return JsonResponse({"error": "Invalid request"}, status=400)


# --------------------
# MONTHLY JOB
# --------------------
def monthly_job(request):
    if not request.session.get('access_monthly_job'):
        return redirect("/hostel/access/?next=/hostel/monthly_job/")  # ✅ FIXED

    now = timezone.now()
    year = int(request.GET.get("year", now.year))
    month = int(request.GET.get("month", now.month))

    job_list = MonthlyJob.objects.all().order_by('id')
    records = MonthlyJobRecord.objects.filter(year=year, month=month)

    record_map = {r.job_id: r for r in records}

    return render(request, "management/monthly_job.html", {
        "joblist": job_list,
        "record_map": record_map,
        "year": year,
        "month": month
    })


def save_payment(request):
    data = json.loads(request.body)

    record, _ = MonthlyJobRecord.objects.get_or_create(
        job_id=data["job_id"],
        year=data["year"],
        month=data["month"]
    )

    record.payment = data["payment"] or None
    record.save()

    return JsonResponse({"status": "ok"})


def upload_image(request):
    record, _ = MonthlyJobRecord.objects.get_or_create(
        job_id=request.POST.get("job_id"),
        year=request.POST.get("year"),
        month=request.POST.get("month")
    )

    img = MonthlyJobImage.objects.create(
        record=record,
        image=request.FILES.get("image")
    )

    return JsonResponse({"url": img.image.url})


def mark_done(request):
    data = json.loads(request.body)

    record, _ = MonthlyJobRecord.objects.get_or_create(
        job_id=data["job_id"],
        year=data["year"],
        month=data["month"]
    )

    record.is_done = True
    record.save()

    return JsonResponse({"status": "done"})


# --------------------
# RESTAURANT
# --------------------
def r_order(request):
    return render(request, "restaurant/order.html")