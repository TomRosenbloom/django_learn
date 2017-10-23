from django import forms
from backend.models import Organisation, OrganisationType, Opportunity

from localflavor.gb.forms import GBPostcodeField

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OpportunityForm(forms.ModelForm):

    class Meta:
        model = Opportunity
        fields = ('name','description','start_date','end_date')
        labels = {'name': 'Opportunity title'}



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', )
