from django import forms


class PresentationForm(forms.Form):
    lection_name = forms.CharField()
    lector_data = forms.CharField()
    logo = forms.FileField()
    text = forms.FileField()

