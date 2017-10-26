from django import forms
from backend.models import OrganisationType, OrganisationRegistration

class OrganisationtypeForm(forms.ModelForm):

    class Meta:
        model = OrganisationType
        fields = '__all__'

class OrganisationRegistrationForm(forms.ModelForm):

    class Meta:
        model = OrganisationRegistration
        fields = ('type','reg_number')
