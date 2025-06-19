from django import forms

class TimeCheckoutForm(forms.Form):
    time_tag = forms.CharField(required=True)
    time_switch = forms.CharField(required=False)
    time_correction = forms.DateTimeField(required=False)


class SettingsForm(forms.Form):
    setting_tag = forms.CharField(
        label='tag:',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-check',
            'placeholder': 'Tag Name',
        })
    )
    setting_type = forms.CharField(required=True)


class DeleteTagForm(forms.Form):
    selecting_tag = forms.CharField(required=True)


class RecordDel(forms.Form):
    del_id = forms.IntegerField()