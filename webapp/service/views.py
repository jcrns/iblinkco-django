from django.shortcuts import render, redirect

# Importing profile update form
from users.forms import ProfileUpdateForm

# Importing job posting form
from .forms import JobPostForm

# Importing lib to get specific objects
from django.shortcuts import get_object_or_404

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
        # print(form.cleaned_data.get('instagram'))
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
            print("instagramBool ", instagramBool)
            print("facebookBool ", facebookBool)
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
            print('sefbierfgrfyfew')
            print(number_of_post)
            
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
                # return redirect('dashboard-confirm-job', pk=job_id)
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
def completeProfile(request):
    if request.method == 'POST':
        
        # Creating form with post data
        form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        print(form)
        
        # Checking if form is valid
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('dashboard-home')
        else:
            print(form.errors)
            return redirect('service-complete-profile')
    # Defining form and user
    form = ProfileUpdateForm
    user = request.user

    # Defining profile
    profile = request.user.profile

    # Checking if client is requesting else redirecting home
    if profile.is_client == True:
        # Checking if client has updated previously
        if profile.business_type == 'none':
            return render(request, 'service/complete_profile.html', { 'form' : form, "nav_black_link" : True })
        else:
            return redirect('dashboard-home')
    else:
        return redirect('homepage-home')

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
    print("platforms: ", platforms)
    post_per_day= float(post_per_day) * 0.375
    print("post_per_day: ", post_per_day)

    number_of_services= float(number_of_services) * 0.5
    print("number_of_services: ", number_of_services)

    perDayValue = platforms+post_per_day+number_of_services
    print("perDayValue: ", perDayValue)
    
    # Getting job base cost by multiplying by the length of the job
    length = float(length)
    totalValue = perDayValue * length
    print("Total Base Value: ", totalValue)

    # Adding other services from managers to total
    totalValue = totalValue + engagement
    totalValue = totalValue + post_for_you
    


    # Getting iBlinkco deduction by taking a percent from data
    iblinkcoValue = (totalValue * 0.1 ) + 2
    print("iblinkcoValue: ", iblinkcoValue)
    
    # Adding iBlinkco deduction to total
    totalValue = totalValue + iblinkcoValue

    # Get stripe 
    stripe = (totalValue*0.029) + 0.3
    print("stripe: ", stripe)

    totalValue = totalValue + stripe
    totalValue = round(totalValue, 1)
    print(totalValue)
    return totalValue