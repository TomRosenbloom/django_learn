from django import forms
from backend.models import Organisation, OrganisationType

from localflavor.gb.forms import GBPostcodeField

class OrganisationForm(forms.ModelForm):
    postcode = GBPostcodeField()

    class Meta:
        model = Organisation
        fields = ('organisation_name','types','email','telephone','postcode')
        labels = { 'types': 'Organisation type(s)'}
