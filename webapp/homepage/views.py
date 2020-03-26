from django.shortcuts import render

from django.http import HttpResponse

# Homepage function
def home(request):
    return render(request, 'homepage/index.html')

def termsAndConditions(request):
    return render(request, 'homepage/terms-and-conditions.html')

def privacyPolicy(request):
    return render(request, 'homepage/privacy-policy.html')

def partnerships(request):
    return render(request, 'homepage/partnerships.html')

def helpAndSupport(request):
    return render(request, 'homepage/help-and-support.html')

def becomeManager(request):
    return render(request, 'homepage/become-a-manager.html')