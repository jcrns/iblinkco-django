from django.shortcuts import render, redirect

# Importing User Registeraton Form
from users.forms import UserRegisterForm

# Importing Authentication Form
from django.contrib.auth.forms import AuthenticationForm

# Importing profile to access 
from users.models import Profile

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
    if profile.is_client == True:
        if profile.business_type != 'none':
            return redirect('dashboard-home')
    else:
        if profile.description != 'none':
            return redirect('dashboard-home')
    return render(request, 'homepage/overview.html', {"nav_black_link" : True} )
    
def termsAndConditions(request):
    return render(request, 'homepage/terms-and-conditions.html', {"nav_black_link" : True} )

def privacyPolicy(request):
    return render(request, 'homepage/privacy-policy.html', {"nav_black_link" : True} )

def partnerships(request):
    return render(request, 'homepage/partnerships.html', {"nav_black_link" : True} )

def helpAndSupport(request):
    return render(request, 'homepage/help-and-support.html', {"nav_black_link" : True} )

def becomeManager(request):
    if request.user.is_authenticated:
    
        if request.user.profile.is_client == True:
            return redirect('service-job')
        return render(request, 'homepage/become-a-manager.html', {"nav_black_link" : True} )
    else:
        return redirect('dashboard-home')
