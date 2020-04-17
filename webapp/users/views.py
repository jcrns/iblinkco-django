from django.shortcuts import redirect

from django.http import HttpResponseRedirect

# Importing login func from django
from django.contrib.auth import authenticate, login, logout

# Importing Authentication Form
from django.contrib.auth.forms import AuthenticationForm

# importing messages from django
from django.contrib import messages

# Importing email functions
from django.core.mail import EmailMessage

# Importing to handle Url
from django.urls import reverse
from urllib.parse import urlencode

# importing User Registeraton Form
from .forms import UserRegisterForm, ProfileUpdateFormClient, ProfileUpdateFormManager

# Importing Profile Modal
from .models import Profile

# Importing Evaluation Modal
from management.models import ManagerEvaluation

# Registering new user
def registerFunc(request):
    if request.method == 'POST':

        # Getting posted data in form
        form = UserRegisterForm(request.POST)

        # Checking if form is valid
        if form.is_valid():
            form.save()

            # Getting username and email to create message and confirm email
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            # Creating thank you message
            messages.success(request, f'Congratulations {username} you created an account for iBlinkco!')

            # Sending email 
            email = EmailMessage('Welcome to iBlinkco', 'Thank you for signing up to iBlinkco', to=[f'{email}'])
            print(email)
            email.send()
            print({email})
            
            # Redirecting to login screen
            url = createUrl('login')
            return redirect(url)
        else:
            messages.warning(request, f'There was a problem creating your account')
            

            # Redirecting to signup screen
            url = createUrl('signup')
            return redirect(url)

    # Redirecting to signup screen
    url = createUrl('signup')
    return redirect(url)

# Login function
def loginFunc(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(user)
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect('dashboard-home')
        else:
            # Redirecting to signup screen
            messages.warning(request, f'There was a problem logging in your account')
            url = createUrl('login')
            return redirect(url)
    else:
        form = AuthenticationForm()
    return redirect('homepage-home')

# Logout function
def logoutFunc(request):
    # user = request.user
    logout(request)
    return redirect('dashboard-home')

# PROFILE FUNC

# Choose type of user function
def comfirmUser(request):
    if request.method == 'POST':

        managerOrClient = request.POST.get("if-manager-or-client")

        # Getting user
        profile = request.user.profile

        # If Client
        if managerOrClient == 'True':
            # Changing value of manager type
            profile.is_manager = False
            profile.is_client = True

            # Saving value in db
            profile.save(update_fields=["is_manager", "is_client"])
            
            # Redirecting 
            return redirect('service-complete-profile-client')
        # If Manager
        else:
            # Changing value of manager type
            profile.is_manager = True
            profile.is_client = False
            
            # Saving value in db
            profile.save(update_fields=["is_manager", "is_client"]) 
            
            # Creating evaluation modal for managers
            evaluation = ManagerEvaluation()
            evaluation.manager = request.user
            evaluation.save()

            # Redirecting 
            return redirect('service-complete-profile-manager')

        
        return redirect('homepage-home')

# Function to create url with paramaters
def createUrl(state):
    base_url = reverse('homepage-home')
    if state == 'login':
        query_string =  urlencode({'login': 'true'})
    elif state == 'signup':
        query_string =  urlencode({'signup': 'true'})
    url = '{}?{}'.format(base_url, query_string) 
    return url