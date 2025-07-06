from django import forms

class TimeCheckoutForm(forms.Form):
    time_tag = forms.CharField(required=True)
    time_switch = forms.BooleanField(required=False)
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


class ExcelUploadForm(forms.Form):
    file = forms.FileField(label='Upload Excel File')


class MedicineForm(forms.Form):
    medicine_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-check',
            'placeholder': '',
        })
    )


class MedicineRecordForm(forms.Form):
    med_name = forms.CharField(required=True)


class DeleteMedForm(forms.Form):
    selecting_med = forms.IntegerField(required=True)


class WeightForm(forms.Form):
    weight_Morning = forms.CharField(label="",
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Morning'}),
                            required=False)
    weight_BeforeLunch = forms.CharField(label="",
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Before Lunch'}),
                            required=False)
    weight_AfterLunch = forms.CharField(label="",
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'After Lunch'}),
                            required=False)
    weight_Sleep = forms.CharField(label="",
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Sleep'}),
                            required=False)