from django.shortcuts import render
from .models import BlogPost

# Homepage function
def home(request):
    content = {
        'posts': BlogPost.objects.all()
    }
    return render(request, 'blog/blog.html', content)