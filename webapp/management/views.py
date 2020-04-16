from django.shortcuts import render, redirect

# Importing profile to access 
from .models import ManagerEvaluation

# Importing lib to get specific objects
# from django.shortcuts import get_object_or_404

# Importing login required func
from django.contrib.auth.decorators import login_required

# Homepage function
@login_required(login_url="/?login=true")
def evaluation(request):
    profile = request.user.profile
    if profile.is_manager == True:
        if profile.evaluation == False:
            return render(request, 'management/evaluation.html')
        else:
            return redirect('dashboard-home')
    else:
        return redirect('dashboard-home')