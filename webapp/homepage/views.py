from django.shortcuts import render, redirect

from django.http import HttpResponse

# Importing User Registeraton Form
from users.forms import UserRegisterForm

# Importing Authentication Form
from django.contrib.auth.forms import AuthenticationForm

# Importing profile to access 
from users.models import Profile

# Importing lib to get specific objects
# from django.shortcuts import get_object_or_404

# Importing login required func
from django.contrib.auth.decorators import login_required

# Homepage function
def home(request):
    form_register = UserRegisterForm()
    form_login = AuthenticationForm()
    return render(request, 'homepage/index.html', {'form_register': form_register, 'form_login' : form_login })

# Overview function
@login_required(login_url="/?login=true")
def overview(request):
    profile = request.user.profile
    print(profile.business_type)
    if profile.business_type != 'none':
        return redirect('dashboard-home')
    return render(request, 'homepage/overview.html')
    
def termsAndConditions(request):
    return render(request, 'homepage/terms-and-conditions.html')

def privacyPolicy(request):
    return render(request, 'homepage/privacy-policy.html')

def partnerships(request):
    return render(request, 'homepage/partnerships.html')

def helpAndSupport(request):
    return render(request, 'homepage/help-and-support.html')

def becomeManager(request):
    return render(request, 'homepage/become-a-manager.html')