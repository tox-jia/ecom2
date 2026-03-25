from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Guest, Term
from .forms import CheckinForm


def checkin(request):
    if request.method == "POST":
        form = CheckinForm(request.POST, request.FILES)
        if form.is_valid():
            guest = form.save()

            # save session
            request.session['guest_id'] = guest.id
            request.session['answers'] = {}  # reset answers

            return redirect('terms', step=1)
    else:
        form = CheckinForm()

    return render(request, 'hostel/checkin.html', {'form': form})


def terms(request, step):
    # 🔒 prevent skipping
    guest_id = request.session.get('guest_id')
    if not guest_id:
        return redirect('checkin')

    terms_list = list(Term.objects.all())

    # 🛑 prevent crash
    if step > len(terms_list):
        return redirect('summary')

    term = terms_list[step - 1]

    if request.method == "POST":
        answer = request.POST.get('answer')

        # ❌ wrong answer → block
        if answer != term.correct_answer:
            messages.error(
                request,
                term.warning_message or "Please select the correct answer."
            )
            return redirect('terms', step=step)

        # ✅ save correct answer
        answers = request.session.get('answers', {})
        answers[str(term.id)] = answer
        request.session['answers'] = answers

        # ➡️ next step
        if step < len(terms_list):
            return redirect('terms', step=step + 1)
        else:
            return redirect('summary')

    return render(request, 'hostel/terms.html', {
        'term': term,
        'step': step,
        'total': len(terms_list)
    })


def summary(request):
    guest_id = request.session.get('guest_id')
    if not guest_id:
        return redirect('checkin')

    guest = Guest.objects.get(id=guest_id)
    answers = request.session.get('answers', {})

    # save to DB
    guest.terms_answers = answers
    guest.save()

    terms = Term.objects.all()

    return render(request, 'summary.html', {
        'guest': guest,
        'answers': answers,
        'terms': terms
    })


def viewGuest(request, pk):
    guest = get_object_or_404(Guest, pk=pk)
    return render(request, 'hostel/view_guest.html', {'guest': guest})