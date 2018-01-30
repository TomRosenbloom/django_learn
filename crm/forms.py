from django import forms
from backend.models import OrganisationType, OrganisationRegistration

class OrganisationtypeForm(forms.ModelForm):

    class Meta:
        model = OrganisationType
        fields = '__all__'

class OrganisationRegistrationForm(forms.ModelForm):
    """
    Used to define organisation registration i.e. the type(s) of the organisation and any associated registration number
    Used in for e.g. organisation update page in conjunctiuon with organisatin form
    to allow creation of multiple formsets for multiple types 
    """
    class Meta:
        model = OrganisationRegistration
        fields = ('type','reg_number')
