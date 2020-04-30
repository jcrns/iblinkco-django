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

# Creating func to look for manager every five minutes
@shared_task
def check_verification(pk, current_site):
    pass
    # print('dfdfdfdfdf')

    # try:
    #     print('sdsffafdvefge')
    #     job_obj = JobPost.objects.get(pk=pk)

    #     # Checking if manager already assigned if so returning
    #     if job_obj.manager:
    #         return None

    #     # Getting client
    #     client_name = job_obj.client
    #     client = User.objects.get(username=client_name)

    #     # Getting capable managers with filter
    #     managers = Profile.objects.filter(
    #         is_manager=True, language=client.profile.language)

    #     # Randomly selecting managers
    #     manager_name = random.choice(managers)
    #     print(manager_name)
    #     manager = User.objects.get(username=manager_name)

    #     # Emailing manager about job
    #     email = emailJobOffer(manager, job_obj, current_site)

    #     print('complete')
    #     # Saving manager
    #     # job_obj.manager = manager
    #     # job_obj.save()

    #     # Send manager found alert email
    #     # email = EmailMessage(
    #     #     'Congrats we found a manager for your job', 'Hello '+ client + ', We hope all is well, ' + manager_name + ' has been assigned to your job. ', to=[f'{client.email}'])
    #     # print(email)
    #     # email.send()
    #     # print({email})

    #     return None

    # except Exception as e:
    #     print("e")
    #     print(e)
