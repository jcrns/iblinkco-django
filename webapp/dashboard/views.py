from django.shortcuts import render, redirect

# Lib to require login for certain views
from django.contrib.auth.decorators import login_required

# Importing profile to access 
from users.models import Profile

# Importing Complete Profile
from users.forms import ProfileUpdateForm

# Importing lib to get specific objects
# from django.shortcuts import get_object_or_404

# Overview function
@login_required(login_url="/?login=true")
def dashboard(request):
    # Getting user
    profile = request.user.profile
    if profile.is_client == True:
        if profile.business_type != 'none':
            currentJob = None
            past_orders = None
            update_profile_form = ProfileUpdateForm(instance=request.user.profile)
            # Checking if request used post method
            if request.method == 'POST':
        
                # Creating update profile form with post data
                update_profile_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profile)
                
                # Checking if update profile form is valid
                if update_profile_form.is_valid():
                    profile = update_profile_form.save(commit=False)
                    profile.user = request.user
                    profile.save()
                    return redirect('dashboard-home')
            return render(request, 'dashboard/client.html', { 'profile': profile, 'current_job' : currentJob, 'past_orders' : past_orders, 'update_profile_form' : update_profile_form } )
        else:
            return redirect('homepage-home')
    else:
        return render(request, 'dashboard/manager.html')
    


