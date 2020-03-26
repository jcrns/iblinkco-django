from django.shortcuts import render

from django.http import HttpResponse

# Users function
def signUp(request):
    return render(request, 'users/signup-page.html')

def login(request):
    return render(request, 'users/login-page.html')