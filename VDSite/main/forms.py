from django import forms

class UploadedFileForm(forms.Form):
    name = forms.CharField(label='upForm', max_length=100)
    file = forms.FileField()