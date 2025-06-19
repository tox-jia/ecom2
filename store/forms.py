from importlib.metadata import requires

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import Profile


class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(label="",
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}),
                            required=False)
    address1 = forms.CharField(label="",
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 1'}),
                            required=False)
    address2 = forms.CharField(label="",
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 2'}),
                            required=False)
    city = forms.CharField(label="",
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}),
                            required=False)
    state = forms.CharField(label="",
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}),
                            required=False)
    zipcode = forms.CharField(label="",
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}),
                            required=False)
    country = forms.CharField(label="",
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}),
                            required=False)

    class Meta:
        model = Profile
        fields = ('phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'country', )


# class ChangePasswordForm(SetPasswordForm):
#   # class Meta:
    #     model = User
    #     fields = ['new_password1', 'new_password2']
    #
    # def __init__(self, *args, **kwargs):
    #     super(ChangePasswordForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['new_password1'].widget.attrs['class'] = 'form-control'
    #     self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
    #     self.fields['new_password1'].label = ''
    #     self.fields[
    #         'new_password1'].help_text = ('<ul class="form-text text-muted small">'
    #                                       '<li>Your password can\'t be too similar to your other personal information.</li>'
    #                                       '<li>Your password must contain at least 8 characters.</li>'
    #                                       '<li>Your password can\'t be a commonly used password.</li>'
    #                                       '<li>Your password can\'t be entirely numeric.</li></ul>')
    #
    #     self.fields['new_password2'].widget.attrs['class'] = 'form-control'
    #     self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
    #     self.fields['new_password2'].label = ''
    #     self.fields[
    #         'new_password2'].help_text = ('<span class="form-text text-muted">'
    #                                       '<small>Enter the same password as before, for verification.</small></span>')


TIMEZONE_CHOICES = [
    ('Etc/GMT-14', 'GMT+14'),
    ('Etc/GMT-13', 'GMT+13'),
    ('Etc/GMT-12', 'GMT+12, '),
    ('Etc/GMT-11', 'GMT+11, New Zealand'),
    ('Etc/GMT-10', 'GMT+10, Sydney'),
    ('Etc/GMT-9', 'GMT+9, Japan, Korea'),
    ('Etc/GMT-8', 'GMT+8, China, Philippine'),
    ('Etc/GMT-7', 'GMT+7, Thailand, Laos'),
    ('Etc/GMT-6', 'GMT+6, Kazakhstan'),
    ('Etc/GMT-5', 'GMT+5, Pakistan'),
    ('Etc/GMT-4', 'GMT+4, Oman'),
    ('Etc/GMT-3', 'GMT+3, Moscow, Turkey'),
    ('Etc/GMT-2', 'GMT+2, Egypt, Ukraine'),
    ('Etc/GMT-1', 'GMT+1, Germany, France, Sweden'),
    ('Etc/GMT-0', 'GMT-0, London, Iceland'),
    ('Etc/GMT+1', 'GMT-1'),
    ('Etc/GMT+2', 'GMT-2'),
    ('Etc/GMT+3', 'GMT-3, Sao Paulo, Greenland'),
    ('Etc/GMT+4', 'GMT-4, Caracas, Buenos Aires'),
    ('Etc/GMT+5', 'GMT-5, New York, Toronto, Lima'),
    ('Etc/GMT+6', 'GMT-6, Mexico City, Chicago'),
    ('Etc/GMT+7', 'GMT-7, Denver, Edmonton'),
    ('Etc/GMT+8', 'GMT-8, Los Angeles, Vancouver'),
    ('Etc/GMT+9', 'GMT-9, Anchorage'),
    ('Etc/GMT+10', 'GMT-10, Hawaii'),
    ('Etc/GMT+11', 'GMT-11'),
    ('Etc/GMT+12', 'GMT-12'),
]

class UpdateUserForm(forms.ModelForm):
    timezone = forms.ChoiceField(choices=TIMEZONE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Profile
        fields = ('timezone', )




# class UpdateUserForm(UserChangeForm):
#     # hide password section
#     password = None
#     email = None
#     # first_name = forms.CharField(label="", max_length=100,
#     #                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
#     # last_name = forms.CharField(label="", max_length=100,
#     #                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
#     timezone = forms.CharField(label="", max_length=100,
#                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Time Zone', 'value': 'Etc/GMT-8'}))
#
#     class Meta:
#         model = Profile
#         # fields = ('username', 'first_name', 'last_name', 'email')
#         fields = ('timezone',)
#     def __init__(self, *args, **kwargs):
#         super(UpdateUserForm, self).__init__(*args, **kwargs)
#
#         self.fields['timezone'].widget.attrs['class'] = 'form-control'
#         self.fields['timezone'].widget.attrs['placeholder'] = 'GMT + 8, China, Philippine'
#         self.fields['timezone'].label = ''
#         self.fields['timezone'].help_text = ('<span class="form-text text-muted">'
#                                               'GMT + 8, China, Philippine: Etc/GMT-8</span>')

        # ----------------------------------------------

        # self.fields['first_name'].widget.attrs['class'] = 'form-control'
        # self.fields['first_name'].widget.attrs['placeholder'] = 'Given Name'
        # self.fields['first_name'].label = ''
        # self.fields['first_name'].help_text = ('<span class="form-text text-muted">'
        #                                      'Given Name</span>')
        #
        # self.fields['last_name'].widget.attrs['class'] = 'form-control'
        # self.fields['last_name'].widget.attrs['placeholder'] = 'Family Name'
        # self.fields['last_name'].label = ''
        # self.fields['last_name'].help_text = ('<span class="form-text text-muted">'
        #                                        'Family Name</span>')




    # def __init__(self, *args, **kwargs):
    #     super(UpdateUserForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['username'].widget.attrs['class'] = 'form-control'
    #     self.fields['username'].widget.attrs['placeholder'] = 'User Name'
    #     self.fields['username'].label = ''
    #     self.fields['username'].help_text = ('<span class="form-text text-muted">'
    #                                          '<small>Required. 150 characters or fewer. '
    #                                          'Letters, digits and @/./+/-/_ only.</small></span>')


# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(label="",
#                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
#                              required=False)
#     # first_name = forms.CharField(label="", max_length=100,
#     #                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
#     #                              required=False)
#     # last_name = forms.CharField(label="", max_length=100,
#     #                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
#     #                             required=False)
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')
#         # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
#
#     def __init__(self, *args, **kwargs):
#         super(SignUpForm, self).__init__(*args, **kwargs)
#
#         self.fields['username'].widget.attrs['class'] = 'form-control'
#         self.fields['username'].widget.attrs['placeholder'] = 'User Name'
#         self.fields['username'].label = ''
#         self.fields['username'].help_text = ('<span class="form-text text-muted">'
#                                              '<small>'
#                                              'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
#                                              '</small>'
#                                              '</span>')
#
#         self.fields['password1'].widget.attrs['class'] = 'form-control'
#         self.fields['password1'].widget.attrs['placeholder'] = 'Password'
#         self.fields['password1'].label = ''
#         self.fields['password1'].help_text = ('<ul class="form-text text-muted small">'
#                                               '<li>'
#                                               'Your password can\'t be too similar to your other personal information.'
#                                               '</li>'
#                                               '<li>'
#                                               'Your password must contain at least 8 characters.'
#                                               '</li>'
#                                               '<li>'
#                                               'Your password can\'t be a commonly used password.'
#                                               '</li>'
#                                               '<li>'
#                                               'Your password can\'t be entirely numeric.'
#                                               '</li>'
#                                               '</ul>')
#
#         self.fields['password2'].widget.attrs['class'] = 'form-control'
#         self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
#         self.fields['password2'].label = ''
#         self.fields['password2'].help_text = ('<span class="form-text text-muted">'
#                                               '<small>'
#                                               'Enter the same password as before, for verification.'
#                                               '</small>'
#                                               '</span>')



