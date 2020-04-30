from django.shortcuts import render, redirect

# Importing login required func
from django.contrib.auth.decorators import login_required

# Importing profile update form
from users.forms import ProfileUpdateFormClient, ProfileUpdateFormManager

# Importing job posting form
from .forms import JobPostForm

# Importing job model
from .models import JobPost

# Importing profile model
from users.models import Profile

# Importing messages
from django.contrib import messages

# Adding random string gen to create job id
from webapp.utils import unique_order_id_generator

# Importing billing
from billing.models import BillingProfile

# Importing stripe
import stripe

# Importing celery task
from .tasks import manager_assignment, check_milestone_date
from datetime import timedelta, datetime

# Importing lib to get base site
from django.contrib.sites.shortcuts import get_current_site

# Importing stripe key for checkout
stripe.api_key = "sk_test_8dRE7QLn40wUt6wZtr8upMA4"


# View for django post job select
def postJobSelect(request):

    # Defining profile
    profile = request.user.profile
 
    # Checking if user is client
    if profile.is_client == True:
        if profile.busy == False:
            return render(request, 'service/post_job_select.html', { "static_header" : True, "nav_black_link" : True })
        else:
            return redirect('dashboard-home')
    else:
        return redirect('homepage-home')

# View for post job custom
def postJob(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        profile = request.user.profile
        if form.is_valid():
            print(form)
            # Getting posted fields
            post_per_day = form.cleaned_data.get('number_of_post')
            length = form.cleaned_data.get('length')
            instagramBool = form.cleaned_data.get('instagram')
            instagramUsername = form.cleaned_data.get('instagram_username')
            facebookBool = form.cleaned_data.get('facebook')
            facebookUsername = form.cleaned_data.get('facebook_username')
            engagement = form.cleaned_data.get('engagement')
            post_for_you = form.cleaned_data.get('post_for_you')
            captions = form.cleaned_data.get('captions')
            search_for_content = form.cleaned_data.get('search_for_content')
            
            price = calculatePrice(post_per_day, length, instagramBool, facebookBool, engagement, post_for_you, captions, search_for_content)
            
            # Validating Instagram and Twitter info is appropriate
            if instagramBool == False and facebookBool == False:
                return redirect('service-job')
                
            if instagramBool == True:
                if not instagramUsername:
                    messages.warning(request, f'Please Enter Instagram Username')
                    return redirect('service-job')
            else:
                instagramUsername == 'none'
            
            if facebookBool == True:
                if not facebookUsername:
                    messages.warning(request, f'Please Enter Facebook Username')
                    return redirect('service-job')
            else:
                facebookUsername == 'none'
            
            # Getting total number of expected post throughout the job
            number_of_post = int(post_per_day) * int(length) 
            
            # Checking if user is currently in a job
            if profile.busy == False:
                # Saving job in db
                job = form.save()
                job.client = request.user
                
                # Assigning variables to post to form
                job.number_of_post = number_of_post
                job.price_paid = price
                job.save()

                # Updating profile to busy
                profile.busy = True
                profile.save(update_fields=["busy"])

                # Get obj for redirect
                job = JobPost.objects.get(client=request.user)
                pk = job.pk
                
                # getting current site and passing in to func
                current_site = get_current_site(request)
                current_site = current_site.domain

                # Running async manager selection function
                manager_assignment.apply_async((pk, current_site), countdown=3)
                return redirect('dashboard-confirm-job', pk=pk)
            return redirect('dashboard-home')
        else:
            print(form.errors)
    form = JobPostForm
    user = request.user
    profile = request.user.profile
    if profile.is_client == True:
        if profile.busy is not True:
            return render(request, 'service/post_job.html', { 'form' : form, "static_header" : True, "nav_black_link" : True })
        else:
            return redirect('dashboard-home')
    else:
        return redirect('homepage-home')

# View for complete profile screen
@login_required(login_url="/?login=true")
def completeProfileClient(request):
    if request.method == 'POST':
        
        # Creating form with post data
        form = ProfileUpdateFormClient(request.POST or None, request.FILES or None, instance=request.user.profile)
        print(form)
        
        # Checking if form is valid
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, f'User profile completed')
            return redirect('dashboard-home')
        else:
            print(form.errors)
            return redirect('service-complete-profile-client')
    # Defining form and user
    form = ProfileUpdateFormClient
    user = request.user

    # Defining profile
    profile = request.user.profile

    # Checking if client is requesting else redirecting home
    if profile.is_client == True:
        # Checking if client has updated previously
        if profile.business_type == 'none':
            return render(request, 'service/complete_profile_client.html', { 'form' : form, "nav_black_link" : True })
        else:
            return redirect('dashboard-home')
    else:
        return redirect('homepage-home')

# View for complete profile screen
@login_required(login_url="/?login=true")
def completeProfileManager(request):
    if request.method == 'POST':
        
        # Creating form with post data
        form = ProfileUpdateFormManager(request.POST or None, request.FILES or None, instance=request.user.profile)
        print(form)
        
        # Getting dob
        dob = form.cleaned_data.get('date_of_birth')
        print(dob)

        # Converting dob to datetime obj using current time
        my_time = datetime.min.time()
        dob = datetime.combine(dob, my_time)

        # Checking age with dob
        now = datetime.now()
        age = int((now - dob).days)
        age = age/365

        if age < 18:
            messages.warning(request, f'You have to be at least 18 years old to sign up as a manager')
            return redirect('service-complete-profile-manager')
        print(age)

        # Checking if form is valid
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, f'User profile completed')
            return redirect('management-evaluation')
        else:
            print(form.errors)
            return redirect('service-complete-profile-manager')
            
    # Defining form and user
    form = ProfileUpdateFormManager
    user = request.user

    # Defining profile
    profile = request.user.profile

    # Checking if client is requesting else redirecting home
    if profile.is_manager == True:
        # Checking if client has updated previously
        if profile.business_type == 'none':
            return render(request, 'service/complete_profile_manager.html', { 'form' : form, "nav_black_link" : True })
        else:
            return redirect('dashboard-home')
    else:
        return redirect('homepage-home')


# Checkout view
def checkoutHome(request, job_id):

    # Getting job
    job_obj = JobPost.objects.get(job_id=job_id)

    # Redirecting if job is paid for
    if job_obj.paid_for == True:
        return redirect('dashboard-home')

    # Getting managers stripe uid uid to 
    manager_name = job_obj.manager
    manager = Profile.objects.get(user=manager_name)
    manager_uid = manager.stripe_user_id

    # Creating payment object
    payment_intent = stripe.PaymentIntent.create(
        payment_method_types=['card'],
        amount=3000,
        currency='usd',
        application_fee_amount=123,
        transfer_data={
            'destination': manager_uid,
        }
    )
    # Checking if manager is selected if not redirecting
    if not job_obj.manager:
        return redirect('dashboard-home')

    return render(request, 'service/checkout.html', {"object": job_obj, "client_secret": payment_intent.client_secret, "static_header": True, "nav_black_link": True})


# def charge(request):
#     job = JobPost.objects.get(client=request.user)
#     if request.method == "POST":

#         # Creating stripe customer
#         customer = stripe.Customer.create(
#             email=request.user.email,
#             name=request.user.username,
#             source=request.POST['stripeToken']
#         )

#         # Converting price to pennies for stripe
#         price = int(job.price_paid*100)

#         # Charging user
#         charge = stripe.Charge.create(
#             customer=customer,
#             amount=price,
#             currency="usd",
#             description=job.service_description
#         )
        
#         # Changing paid for bool in db
#         job.paid_for = True
#     return redirect('service-job-success', job_id=job.job_id)

# Success view after job is paid for
def jobSuccess(request, job_id):

    job = JobPost.objects.get(client=request.user)
    if job.paid_for == False:
        job.paid_for = True
        job.save()

    # Creating milestone emails

    return render(request, 'service/job_success.html', {"static_header": True, "nav_black_link": True})

# Price calculation func
def calculatePrice(post_per_day, length, instagramBool, facebookBool, engagement, post_for_you, caption, search_for_content):
    platforms = 0
    number_of_services = 0

    # Checking number of platforms
    if instagramBool == True:
        platforms += 1
    if facebookBool == True:
        platforms += 1
    

    # Checking number of services
    if caption == True:
        number_of_services += 1
    if search_for_content == True:
        number_of_services += 1
    
    # Checking if additional services provided by managers are true
    if engagement == True:
        engagement = 2
    else:
        engagement = 2

    if post_for_you == True:
        post_for_you = 5
    else:
        post_for_you = 5

    # Adjusting prices
    platforms= float(platforms) * 0.375
    post_per_day= float(post_per_day) * 0.375

    number_of_services= float(number_of_services) * 0.5

    perDayValue = platforms+post_per_day+number_of_services
    
    # Getting job base cost by multiplying by the length of the job
    length = float(length)
    totalValue = perDayValue * length

    # Adding other services from managers to total
    totalValue = totalValue + engagement
    totalValue = totalValue + post_for_you
    


    # Getting iBlinkco deduction by taking a percent from data
    iblinkcoValue = (totalValue * 0.1 ) + 2
    
    # Adding iBlinkco deduction to total
    totalValue = totalValue + iblinkcoValue

    # Get stripe 
    stripe = (totalValue*0.029) + 0.3

    totalValue = totalValue + stripe
    totalValue = round(totalValue, 1)
    return totalValue
