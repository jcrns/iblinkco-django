from django.shortcuts import render, redirect

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

        # Checking if evaluation process has started
        if profile.evaluated == False:
            if evaluation.evaluation_started == False:

                if request.method == 'POST':
                    print('sfeirjkgerybuguiergu')

                    # Changing value of evaluated bool in db to move on
                    evaluation.evaluation_started = True
                    evaluation.save()

                    # Redirecting
                    return redirect('management-evaluation')
                return render(request, 'management/evaluation_start.html', {"static_header" : True, "nav_black_link" : True })
            # Checking if first question is answered
            elif evaluation.answer_one_caption_one == 'none' and evaluation.answer_one_caption_two == 'none' and evaluation.answer_one_caption_three == 'none':
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

                return render(request, 'management/evaluation_one.html', {"form": form, "static_header" : True, "nav_black_link" : True })
            elif evaluation.answer_two == 'none' and evaluation.answer_two_img is None:
                return render(request, 'management/evaluation_two.html', {"static_header" : True, "nav_black_link" : True })
            elif evaluation.answer_three == 'none':
                return render(request, 'management/evaluation_two.html', {"static_header" : True, "nav_black_link" : True })
            else:
                return redirect('dashboard-home')
        else:
                return redirect('dashboard-home')
    else:
        return redirect('dashboard-home')