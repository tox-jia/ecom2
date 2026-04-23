from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Guest, Term
from .forms import CheckinForm


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
def viewGuest(request, pk):
    guest = get_object_or_404(Guest, pk=pk)
    return render(request, 'hostel/view_guest.html', {'guest': guest})