from django import forms
from backend.models import Person

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name','last_name','title','dob','sex','mobile','email','address']


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
