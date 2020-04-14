from django.shortcuts import render, redirect

# Importing profile update form
from users.forms import ProfileUpdateForm

# Importing job posting form
from .forms import JobPostForm

# Importing lib to get specific objects
# from django.shortcuts import get_object_or_404

# View for django post job select
def postJobSelect(request):

    # Defining profile
    profile = request.user.profile
    
    # Checking if user is client
    if profile.is_client == True:
        if profile.busy is not True:
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
            
            # Assigning variables to post to form
            form.number_of_post = number_of_post

            if profile.busy == False:
                # Saving job in db
                job = form.save(commit=True)
                job.client = request.user
                job.save()

                # Updating profile to busy
                profile.busy == True
                profile.save(update_fields=["busy"])

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