from django.shortcuts import render

from django.contrib.auth.decorators import login_required

# Overview function
@login_required(login_url="/?login=true")
def overview(request):
    return render(request, 'dashboard/overview.html')
