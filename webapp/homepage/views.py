from django.shortcuts import render

from django.http import HttpResponse

# Homepage function
def home(request):
    return render(request, 'homepage/index.html')

