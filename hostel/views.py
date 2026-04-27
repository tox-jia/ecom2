from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Guest, Term, RoomState
from .forms import CheckinForm

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# --------------------
# LANGUAGE PAGE
# --------------------
def language(request):
    # Optional: reset session if user wants to restart
    if request.GET.get('reset'):
        request.session.flush()

    return render(request, 'hostel/language.html')


# --------------------
# CHECK-IN
# --------------------
def checkin(request):
    # 🔒 require language first
    lang = request.GET.get('lang')

    # ✅ only set once (LOCK)
    if lang:
        request.session['lang'] = lang

    # 🚫 no language → go back
    if 'lang' not in request.session:
        return redirect('language')

    lang = request.session.get('lang')

    if request.method == "POST":
        form = CheckinForm(request.POST, request.FILES)
        if form.is_valid():
            guest = form.save()

            # save session
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
# TERMS (STEP FLOW)
# --------------------
def terms(request, step):
    # 🔒 must have language
    if 'lang' not in request.session:
        return redirect('language')

    # 🔒 must have started check-in
    guest_id = request.session.get('guest_id')
    if not guest_id:
        return redirect('checkin')

    terms_list = list(Term.objects.all().order_by('id'))
    total = len(terms_list)

    # 🛑 prevent overflow
    if step > len(terms_list):
        return redirect('summary')

    term = terms_list[step - 1]
    lang = request.session.get('lang')

    if request.method == "POST":
        answer = request.POST.get('answer')

        # ❌ wrong answer
        lang = request.session.get('lang')

        if answer != term.correct_answer:
            msg = term.get_warning(lang) or "Invalid answer"
            messages.error(request, msg)
            return redirect('terms', step=step)

        # ✅ save answer
        answers = request.session.get('answers', {})
        answers[str(term.id)] = answer
        request.session['answers'] = answers

        # ➡️ next step
        if step < len(terms_list):
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
    # 🔒 must have language
    if 'lang' not in request.session:
        return redirect('language')

    guest_id = request.session.get('guest_id')
    if not guest_id:
        return redirect('checkin')

    guest = Guest.objects.get(id=guest_id)
    answers = request.session.get('answers', {})

    # save to DB
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
# VIEW GUEST (ADMIN / VIEW)
# --------------------
def gList(request):
    if not request.session.get('access_granted'):
        return redirect(f"/hostel/access/?next=/hostel/glist/")

    guests = Guest.objects.all().order_by('-id')
    rooms = RoomState.objects.all().order_by('-id')
    return render(request, 'hostel/glist.html', {'guest': guests, 'rooms': rooms})


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
    if not request.session.get('access_granted'):
        return redirect(f"/hostel/access/?next=/hostel/clean/")

    rooms = RoomState.objects.all().order_by('id')

    rooms1 = rooms[:8]        # first 8
    rooms2 = rooms[8:20]      # 9–20 (index 8 to 19)
    rooms3 = rooms[20:]       # rest

    return render(request, 'hostel/clean.html', {
        'rooms1': rooms1,
        'rooms2': rooms2,
        'rooms3': rooms3,
    })



def update_room(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        room_id = data.get('id')
        field = data.get('field')

        room = RoomState.objects.get(id=room_id)

        if field == 'out':
            room.out = not room.out
            if not room.out:
                room.key = False
                room.is_clean = False

        elif field == 'key':
            if room.out:
                room.key = not room.key

        elif field == 'clean':
            if room.out:
                room.is_clean = not room.is_clean

        room.save()

        return JsonResponse({
            'out': room.out,
            'key': room.key,
            'is_clean': room.is_clean
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)



def reset_rooms(request):
    if request.method == "POST":
        RoomState.objects.update(
            out=False,
            key=False,
            is_clean=False
        )
        return JsonResponse({"status": "ok"})

    return JsonResponse({"error": "Invalid request"}, status=400)





# --------------------
# PASSWORD
# --------------------

ACCESS_PASSWORD = "122812"  # ← change this to your fixed password


def access_gate(request):
    next_url = request.GET.get('next', '/')

    if request.method == "POST":
        password = request.POST.get("password")

        if password == ACCESS_PASSWORD:
            request.session['access_granted'] = True
            return redirect(next_url)
        else:
            return render(request, "hostel/access.html", {
                "error": "Wrong password",
                "next": next_url
            })

    return render(request, "hostel/access.html", {"next": next_url})