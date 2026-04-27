from importlib.metadata import requires

from django import forms
from .models import Guest


class CheckinForm(forms.ModelForm):
    PLATFORM_CHOICES = [
        ('trip', 'Trip.com'),
        ('booking', 'Booking.com'),
        ('agoda', 'Agoda.com'),
    ]

    givenname = forms.CharField(label="Given Name",
                            widget=forms.TextInput(attrs={'class':'form-control',
                                                          'placeholder':'Given Name'}),
                            required=True)

    surname = forms.CharField(label="Surname",
                            widget=forms.TextInput(attrs={'class':'form-control',
                                                          'placeholder':'Surname'}),
                            required=True)

    platform = forms.ChoiceField(
        label="Platform",
        choices=PLATFORM_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        initial='trip'
    )

    country = forms.CharField(label="Nationality",
                            widget=forms.TextInput(attrs={'class':'form-control',
                                                          'placeholder':'Country'}),
                            required=True)

    start_day = forms.ChoiceField(
        label="Start Date",
        choices=[(i, i) for i in range(1, 32)],
        initial=15,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    end_day = forms.ChoiceField(
        label="Start Date",
        choices=[(i, i) for i in range(1, 32)],
        initial=16,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    passport = forms.ImageField(required=True)
    selfie = forms.ImageField(required=True)


    class Meta:
        model = Guest
        fields = ('givenname', 'surname', 'platform', 'country', 'start_day', 'end_day', 'selfie', 'passport')