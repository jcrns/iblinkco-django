# Importing libs for stripe
import requests
import urllib
import stripe

from django.conf import settings

from django.shortcuts import render, redirect

# importing messages from django
from django.contrib import messages

# Importing profile to access
from users.models import Profile

# Importing job post for job acceptance
from service.models import JobPost

# Importing evaluation modal 
from .models import ManagerEvaluation

# Importing evaluation forms
from .forms import *

# Importing login required func
from django.contrib.auth.decorators import login_required

# Importing email functions
from django.core.mail import EmailMessage

# Importing needed libs for job acceptance
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from webapp.tokens import token_generation

# Homepage function
@login_required(login_url="/?login=true")
def evaluation(request):
    # Getting profile
    profile = request.user.profile

    # Getting user
    user = request.user

    # Getting evaluation object
    evaluation = ManagerEvaluation.objects.get(manager=user)

    # Checking if user is a manager
    if profile.is_manager == True:

        # Creating list for possible locations of answer_two_img
        answer_img_list = ['application_pics/default.jpeg', 'application_pics/default.jpg', 'default.jpeg', 'default.jpg']

        # Checking if evaluation process has started
        if evaluation.accepted == False:
            if evaluation.evaluation_started == False:

                if request.method == 'POST':
                    print('sfeirjkgerybuguiergu')

                    # Changing value of evaluated bool in db to move on
                    evaluation.evaluation_started = True
                    evaluation.save()

                    # Redirecting
                    return redirect('management-evaluation')
                return render(request, 'management/evaluation_start.html', {"static_header" : True, "nav_black_link" : True })
            
            # On first question
            elif evaluation.answer_one_caption_one == 'none' and evaluation.answer_one_caption_two == 'none' and evaluation.answer_one_caption_three == 'none':
                # Getting form
                form = EvaluationOneForm
                
                if request.method == 'POST':

                    # Getting form with inputed data
                    form = EvaluationOneForm(request.POST, instance=evaluation)

                    # Checking if form is valid
                    if form.is_valid():
                        # Saving form
                        # form.save(commit=False)
                        evaluation = form.save(commit=False)
                        evaluation.manager = request.user
                        evaluation.save()
                    
                    # Redirecting
                    return redirect('management-evaluation')
                print("form")
                return render(request, 'management/evaluation_one.html', {"form": form, "static_header" : True, "nav_black_link" : True })
            
            # On second question
            elif evaluation.answer_two_caption == 'none' and evaluation.answer_two_what_are_problems == 'none' and evaluation.answer_two_img in answer_img_list:
                # Getting form
                form = EvaluationTwoForm

                if request.method == 'POST':

                    # Getting form with inputed data
                    form = EvaluationTwoForm(request.POST or None, request.FILES or None, instance=evaluation)
                    
                    # Checking if form is valid
                    if form.is_valid():
                        
                        # Saving form
                        evaluation = form.save(commit=False)
                        evaluation.manager = request.user
                        evaluation.save()
                    else:
                        print(form.errors)
                    return redirect('management-evaluation')
                
                return render(request, 'management/evaluation_two.html', {"form": form, "static_header" : True, "nav_black_link" : True })
            
            # On third question
            elif evaluation.answer_three_caption == 'none' and evaluation.answer_three_img in answer_img_list:
                # Getting form
                form = EvaluationThreeForm

                if request.method == 'POST':

                    # Getting form with inputed data
                    form = EvaluationThreeForm(request.POST or None, request.FILES or None, instance=evaluation)
                    
                    # Checking if form is valid
                    if form.is_valid():
                        
                        # Saving form
                        evaluation = form.save(commit=False)
                        evaluation.manager = request.user
                        evaluation.save()
                    else:
                        print(form.errors)
                    return redirect('management-evaluation')
                return render(request, 'management/evaluation_three.html', {"form": form, "static_header" : True, "nav_black_link" : True })
            # Last question
            else:
                
                if evaluation.evaluation_completed == True:
                    return render(request, 'management/evaluation_complete.html', { "static_header" : True, "nav_black_link" : True } )
                # Getting language from profile
                language = profile.language
                if language == 'English':
                    language = 'Spanish'
                elif language == 'Spanish':
                    language = 'English'

                if request.method == 'POST':


                    # Getting posted value
                    accepted = request.POST.get('accepted-post')
                    
                    # Converting to bool
                    if accepted == 'True':
                        accepted = True
                    else:
                        accepted = False
                    
                    # Adding to evaluation
                    evaluation.choose_job = accepted
                    evaluation.evaluation_completed = True
                    
                    # Saving evaluation
                    evaluation.save()

                    # Returning function
                    return redirect('dashboard-home')

                return render(request, 'management/evaluation_four.html', { "language" : language, "static_header" : True, "nav_black_link" : True })
        else:
                return redirect('dashboard-home')
    else:
        return redirect('dashboard-home')


# Stripe auth view
def stripeAuthorizeView(request):

    # Checking if user is signed in
    if not request.user.is_authenticated:
        return redirect('dashboard-home')
    
    # Definning stripe oauth url
    url = 'https://connect.stripe.com/oauth/authorize'

    # Creating parameters
    params = {
        'response_type': 'code',
        'scope': 'read_write',
        'client_id': settings.STRIPE_CONNECT_CLIENT_ID,
        # 'redirect_uri': f'http://localhost:8000/users/oauth/callback'
        'redirect_uri': f'http://iblinkco-django.herokuapp.com/users/oauth/callback'
    }

    # Creating final
    url = f'{url}?{urllib.parse.urlencode(params)}'
    return redirect(url)

# Stripe Oauth callback view
def stripeAuthorizeCallbackView(request):
    user = request.user
    code = request.GET.get('code')
    if not request.user.is_authenticated():
        if code:
            data = {
                'client_secret': settings.STRIPE_SECRET_KEY,
                'grant_type': 'authorization_code',
                'client_id': settings.STRIPE_CONNECT_CLIENT_ID,
                'code': code
            }
            url = 'https://connect.stripe.com/oauth/token'
            resp = requests.post(url, params=data)
            print(resp.json())

            # Updating stipe id token in db
            stripe_user_id = resp.json()['stripe_user_id']
            profile = Profile.objects.get(user=user)
            profile.stripe_user_id = stripe_user_id
            profile.save()
            
    response = redirect('dashboard-home')
    return response
    

# Sending manager email
def emailJobOffer(user, job, current_site):
    
    # Getting current site
    mail_subject = 'Activate your iBlinkco account.'

    # Creating message body and rendering from template
    messageBody = render_to_string('management/job_assignment.html', {
        'user' : user,
        'order': job,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(job.pk)),
        'token': token_generation.make_token(user),
    })
    # Getting email
    email = user.email
    
    print(email)
    
    # Sending email 
    email = EmailMessage(mail_subject, messageBody, to=[f'{email}'])
    email.send()
    return email

# Manager job offer
@login_required(login_url="/?login=true")
def managerOfferConfirm(request, uidb64, token):
    
    # Getting accepted arg
    accepted = request.GET.get('accepted')
    print(accepted)
    # Defining user
    user = request.user
    try:
        # Decoding encoded user id
        uid = force_text(urlsafe_base64_decode(uidb64))

        # Getting user
        job = JobPost.objects.get(pk=uid)
    except:
        job = None
    
    # Checking if job exists
    if job is not None and token_generation.check_token(user, token):

        # If job is accepted changing bool in db
        if accepted == 'True':
            print('sdsdsd')

            # Checking if manager assigned already
            if not job.manager:
                # Changing variable in db
                job.manager = user
                job.save()
                messages.success(request, f'You are now assigned to work a job with {job.client}. We will notfiy when to start the job')
            # Redirecting if manager already assigned
            else:
                messages.warning(request, f'Manager already assigned')
    else:
        messages.warning(request, f'Activation link is invalid!')
    return redirect('dashboard-home')
