from django import forms
from backend.models import Organisation, OrganisationType

from localflavor.gb.forms import GBPostcodeField

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OrganisationForm(forms.ModelForm):
    postcode = GBPostcodeField()

    class Meta:
        model = Organisation
        fields = ('name','types','email','telephone','postcode')
        labels = { 'types': 'Organisation type(s)'}

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', )
