from django import forms
from address.forms import AddressField

class OrganisationAddrForm(forms.Form):
  address = AddressField()

class FormName(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    text = forms.CharField(widget=forms.Textarea)
