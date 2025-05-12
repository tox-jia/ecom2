from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="",
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
                            required=True)
    shipping_email = forms.CharField(label="",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                                required=True)
    shipping_address1 = forms.CharField(label="",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 1'}),
                                required=True)
    shipping_address2 = forms.CharField(label="",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 2'}),
                                required=False)
    shipping_city = forms.CharField(label="",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
                                required=True)
    shipping_state = forms.CharField(label="",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
                                required=False)
    shipping_zipcode = forms.CharField(label="",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}),
                                required=False)
    shipping_country = forms.CharField(label="",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
                                required=True)

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_address1',
                  'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country']
        exclude = ['user',]
        # by grammar, we need a ',' here in exclude


class PaymentForm(forms.Form):
    card_name = forms.CharField(label="", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Name on Card'}))
    card_number = forms.CharField(label="", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Card Number'}))
    card_exp_date = forms.CharField(label="", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Expiration Date'}))
    card_cvv_number = forms.CharField(label="", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'CVV'}))
    card_address1 = forms.CharField(label="", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billing Address 1'}))
    card_address2 = forms.CharField(label="", required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billing Address 2'}))
    card_city = forms.CharField(label="", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billing City'}))
    card_state = forms.CharField(label="", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billing State'}))
    card_zipcode = forms.CharField(label="", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billing Zipcode'}))
    card_country = forms.CharField(label="", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Billing Country'}))
