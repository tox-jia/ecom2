from importlib.metadata import requires

from django import forms
from .models import Guest


class CheckinForm(forms.ModelForm):
    PLATFORM_CHOICES = [
        ('trip', 'Trip.com'),
        ('booking', 'Booking.com'),
        ('agoda', 'Agoda.com'),
    ]

    givenname = forms.CharField(label="",
                            widget=forms.TextInput(attrs={'class':'form-control'}),
                            required=True)

    surname = forms.CharField(label="",
                            widget=forms.TextInput(attrs={'class':'form-control'}),
                            required=True)

    platform = forms.ChoiceField(
        choices=PLATFORM_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    country = forms.CharField(label="",
                            widget=forms.TextInput(attrs={'class':'form-control'}),
                            required=True)

    passport = forms.ImageField(required=True)


    class Meta:
        model = Guest
        fields = ('givenname', 'surname', 'platform', 'country', 'passport')