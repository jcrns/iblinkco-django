# Importing celery
from celery.task.schedules import crontab
from celery import shared_task

# Importing profile and jobpost manager for management assignment
from users.models import Profile
from service.models import JobPost

# Importing email
from django.core.mail import EmailMessage

# Importing random for manager selection
import random

# Importing user model
from django.contrib.auth.models import User

# Importing manager job email func
from management.views import emailJobOffer

# Manager follow up email
@shared_task
def manager_follow_up_email(user):
    try:
        date_joined = user.date_joined
        print(date_joined)
        return None
    except expression as identifier:
        print(identifier)
        return None