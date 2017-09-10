from django.shortcuts import render
from django.views.generic import View, TemplateView, FormView
from . import forms
from .forms import OrganisationForm
from backend.models import OrganisationType, Organisation


from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

class ProfileView(FormView):
    form_class = OrganisationForm
    template_name = 'org_reg/profile.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = OrganisationType.objects.all()
        return context


# class OrgLoginView(TemplateView):
#     template_name = 'org_reg/org_login.html'

def org_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        # check if volunteer/org user
        if hasattr(user, 'profile'):
            profile = user.profile
            is_volunteer = profile.is_volunteer
            is_org_member = profile.is_org_member
        else:
            is_volunteer = is_org_member = 0

        if user and is_org_member:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('org_reg:index'))
            else:
                return HttpResponse("Account not active")
        else:
            if is_volunteer and not is_org_member:
                messages.add_message(
                    request, messages.ERROR, "Volunteer trying to log in as org user"
                    )
            else:
                messages.add_message(
                    request, messages.ERROR, "Incorrect username or password"
                    )
            return HttpResponseRedirect(reverse( 'org_reg:login' ))
    else:
        return render(request,'org_reg/org_login.html',{})

@login_required
def org_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('org_reg:index'))

class OrgSignUpView(TemplateView):
    template_name = 'org_reg/signup.html'

class IndexView(TemplateView):
    template_name = 'org_reg/index.html'
