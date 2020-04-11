from django.shortcuts import render, redirect

# Importing Complete Profile
from users.forms import ProfileUpdateForm

# Importing lib to get specific objects
# from django.shortcuts import get_object_or_404

# Create your views here.
def postJob(request):
    form = None
    user = request.user
    profile = request.user.profile
    if profile.is_client == True:
        return render(request, 'service/post_job.html', { 'form' : form })
    else:
        return redirect('homepage-home')

# Create your views here.
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
            return render(request, 'service/complete_profile.html', { 'form' : form })
        else:
            return redirect('dashboard-home')
    else:
        return redirect('homepage-home')