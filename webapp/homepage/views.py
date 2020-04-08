from django.shortcuts import render, redirect

from django.http import HttpResponse

# Importing User Registeraton Form
from users.forms import UserRegisterForm

# Importing Authentication Form
from django.contrib.auth.forms import AuthenticationForm

# Homepage function
def home(request):
    form_register = UserRegisterForm()
    form_login = AuthenticationForm()
    return render(request, 'homepage/index.html', {'form_register': form_register, 'form_login' : form_login })

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