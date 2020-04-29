# Importing libs for stripe
import requests
import urllib
import stripe

from django.conf import settings

from django.shortcuts import render, redirect

# Importing profile to access
from users.models import Profile

# Importing evaluation modal 
from .models import ManagerEvaluation

# Importing evaluation forms
from .forms import *

# Importing login required func
from django.contrib.auth.decorators import login_required

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
    if not request.user.is_authenticated:
        return redirect('dashboard-home')
    url = 'https://connect.stripe.com/oauth/authorize'
    params = {
        'response_type': 'code',
        'scope': 'read_write',
        'client_id': settings.STRIPE_CONNECT_CLIENT_ID,
        'redirect_uri': f'http://localhost:8000/users/oauth/callback'
    }
    url = f'{url}?{urllib.parse.urlencode(params)}'
    return redirect(url)

# Stripe Oauth callback view


def stripeAuthorizeCallbackView(request):
    code = request.GET.get('code')
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
        profile = Profile.objects.get(user=request.user)
        profile.stripe_user_id = stripe_user_id
        profile.save()
        
        # charge = stripe.Charge.create(
        #     currency='USD',
        #     amount=10000,
        #     source= 'tok_bypassPending'
        # )

        # payout = stripe.Payout.create(
        #     amount=1000,
        #     currency='usd',
        #     # destination=stripe_user_id,
        # )

    response = redirect('dashboard-home')
    return response
