from django import forms
from backend.models import Person

# class RegForm(forms.Form):
#     name = forms.CharField()
#     email = forms.EmailField()
#     text = forms.CharField(widget=forms.Textarea)

class RegForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['forename','surname','title','dob','sex','mobile','email','address']
