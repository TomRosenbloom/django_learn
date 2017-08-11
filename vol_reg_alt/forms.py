from django import forms

#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from backend.models import Profile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password', 'first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ('title','mobile','address')
