# Importing json
import json

from django.shortcuts import render, redirect

# Importing safestring for json
from django.utils.safestring import mark_safe

# Importing login required func
from django.contrib.auth.decorators import login_required

# Importing jobs to access
from service.models import JobPost

# Importing profile to access
from users.models import Profile

# Room for chat
@login_required(login_url="/?login=true")
def room(request, room_name):
    job = JobPost.objects.get(job_id=room_name)
    if not job:
        return redirect('dashboard-home')

    # Checking if user is client or manager then getting opposite
    if request.user == job.client:
        involvedUserName = job.manager
        involvedUser = Profile.objects.filter(user=involvedUserName)
    else:
        involvedUserName = job.client
        involvedUser = Profile.objects.filter(user=involvedUserName)

    return render(request, 'chat/room.html', {
        'room_name': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
        "static_header" : True, 
        "nav_black_link" : True,
        "involvedUser" : involvedUser,
        "involvedUserName" : involvedUserName,
    })