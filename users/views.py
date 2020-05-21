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

# Importing needed libs for email verification
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from webapp.tokens import token_generation

# Registering new user
def registerFunc(request):
    if request.method == 'POST':

        # Getting posted data in form
        form = UserRegisterForm(request.POST)

        # Checking if form is valid
        if form.is_valid():
            # Changing is active bool in database to false before committing
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Getting username and email to create message and confirm email
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            
            # Getting current site
            current_site = get_current_site(request)
            mail_subject = 'Activate your iBlinkco account.'
            
            # Creating message body and rendering from template
            messageBody = render_to_string('users/activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generation.make_token(user),
            })
            # Creating thank you message
            messages.success(
                request, f'Congratulations {username} you created an account for iBlinkco! Please confirm your email address to complete the registration')

            # Sending email 
            email = EmailMessage(mail_subject,
                                 messageBody, to=[f'{email}'])
            print(email)
            email.send()
            
            print('Verification email sent')
            # Redirecting to login screen
            url = createUrl('login')
            return redirect(url)
        else:
            print(form.errors)
            messages.warning(request, f'There was a problem creating your account')
            

            # Redirecting to signup screen
            url = createUrl('signup')
            return redirect(url)

    # Redirecting to signup screen
    url = createUrl('signup')
    return redirect(url)

# Activate account function
def activate(request, uidb64, token):
    try:
        # Decoding encoded user id
        uid = force_text(urlsafe_base64_decode(uidb64))

        # Getting user
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and token_generation.check_token(user, token):

        # Changing value of 
        user.is_active = True
        user.save()
        login(request, user)

        # return redirect('home')
        messages.success(request, f'Thank you for your email confirmation. Now you can login your account.')
    else:
        messages.warning(request, f'Activation link is invalid!')

    # Redirecting to login screen
    return redirect('homepage-overview')

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
            
            # Checking if evaluation is already created if so deleting it
            try:
                evaluation = ManagerEvaluation.objects.get(manager=request.user)
                evaluation.delete()
            except ManagerEvaluation.DoesNotExist:
                print('does not exists')
            

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
            evaluation = ManagerEvaluation.objects.create(manager=request.user)

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
