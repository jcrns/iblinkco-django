# Importing celery
from celery.task.schedules import crontab
from celery.decorators import periodic_task
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

# Importing revoke to end future functions
from celery.task.control import revoke

# Creating func to look for manager every five minutes
@periodic_task(run_every=(crontab(minute='*/20')), ignore_result=True)
def manager_assignment(pk, current_site):
    print('dfdfdfdfdf')
    
    # Checking if we can retrieve job else returning
    try:
        job_obj = JobPost.objects.get(pk=pk)
        print('sdsffafdvefge')

        # Checking if job is none else returning
        if not job_obj:
            revoke('service.tasks.manager_assignment')
            return None

    except Exception as e:
        print(e)
        revoke('service.tasks.manager_assignment')
        return None

    # Trying to get and assign manager and send email
    try:
        # Checking if manager already assigned if so returning
        if job_obj.manager:
            revoke('service.tasks.manager_assignment')
            return None

        # Getting client
        client_name = job_obj.client
        client = User.objects.get(username=client_name)

        # Getting capable managers with filter
        managers = Profile.objects.filter(is_manager=True, language=client.profile.language)
        
        for manager in managers:
            # Randomly selecting managers
            manager_name = random.choice(managers)

            # Getting manager user
            manager = User.objects.get(username=manager_name)

            # Checking if user has stripe connected
            if not manager.profile.stripe_user_id:
                print("manager.profile.stripe_user_id")
                print(manager.profile.stripe_user_id)
                break




        # Emailing manager about job
        email = emailJobOffer(manager, job_obj, current_site)

        print('complete')

        revoke('service.tasks.manager_assignment')
        return None

    except Exception as e:
        print("e")
        print(e)

# Alert milestone email clients
@shared_task
def check_milestone_client_email(pk, milestone):

    try:
        job_obj = JobPost.objects.get(pk=pk)
        print('sdsffafdvefge')

        # Checking if job is none else returning
        if not job_obj:
            revoke('service.tasks.check_milestone_client_email')
            return None

    except Exception as e:
        print(e)
        revoke('service.tasks.check_milestone_client_email')
        return None

    # Check if job still exist if not returning
    try:
        # Getting client and manager for email
        manager = job_obj.manager
        client = job_obj.client

        # Getting client emails
        client = User.objects.get(username=client)
        client_email = str(client.email)

        # Creating str variables
        if milestone == 1:
            milestone = 'One'
            body = 'Hello ' + client + ', We hope all is well, How is your job with ' + manager +' going so far? Make sure to let us know by contacting us at iblinkcompany@gmail.com'
       
        elif milestone == 2:
            milestone = 'Two'
            body = 'Hey ' + client + ', your manager, ' + manager + ' second milestone is due. email us at iblinkcompany@gmail.com. '
       
        elif milestone == 3:
            milestone  = 'Three'
            body = 'Hello ' + client + ', you are more than halfway done with your job with, ' + manager + '. Be sure to email us at iblinkcompany@gmail.com to update us on any problems you are having. '

        elif milestone == 4:
            milestone = 'Four'
            body = 'Hello ' + client + ', your job with, ' + manager + ' will be completed today. Make sure to long into your iBlinkco account now to see the work they have done and to give a rating on their job.  '

        # Sending emails
        
        # Client email
        email = EmailMessage(
            'Milestone ' + milestone + ' Check In', body, to=[f'{client_email}'])
        print(email)
        email.send()
        print({email})

        return None
    except Exception as e:
        print(e)
        return None

# Alert milestone email managers
@shared_task
def milestone_manger_email(pk, milestoneState, warning):
    print('dfdfdfdfdf')

    try:
        job_obj = JobPost.objects.get(pk=pk)
        print('sdsffafdvefge')

        # Checking if job is none else returning
        if not job_obj:
            revoke('service.tasks.milestone_manger_email')
            return None

    except Exception as e:
        print(e)
        revoke('service.tasks.milestone_manger_email')
        return None

    # Checking if we can retrieve job else returning
    try:
        # Getting client and manager for email
        manager = str(job_obj.manager)
        client = str(job_obj.client)

        # Getting client emails
        manager_email = User.objects.get(username=manager)
        print(manager_email)
        manager_email = str(manager_email.email)
        print(manager_email)

        # Creating str variables
        if milestoneState == 1:

            # Checking if this is a warning email
            if warning == True:    
                subject = 'Your First Milestone of your Job With ' + client + ' is Almost Due!'
                body = 'Hello ' + manager + ', We hope all is well, How is your job with ' + client + ' going so far? Make sure to update your first milestone by tomorrow. If you have any questions, contact us at iblinkcompany@gmail.com'
            
            # Sending due email
            else:
                subject = 'Your First Milestone is Due Today!'
                body = 'Hello ' + manager + ', We hope all is well, your first milestone with ' + client + ' is due today. If you have any questions let us know by contacting us at iblinkcompany@gmail.com'

        elif milestoneState == 2:
            if warning == True:

                subject = 'Your Second Milestone of your Job With ' + client + ' is Due Tomorrow!'
                body = 'Hi ' + manager + ', We hope all is well, you are currently working towards you second milestone of your job with ' + client + ' Do not forget to update the milestone on the website and if you have any questions let us know by contacting us at iblinkcompany@gmail.com'
            else:
                subject = 'Your Second Milestone of your Job With ' + client + ' is Due Tomorrow!'
                body = 'Hey ' + manager + ', your manager, ' + manager + ' second milestone is due. email us at iblinkcompany@gmail.com. '

        elif milestoneState == 3:
            if warning == True:
                subject = 'Your Third Milestone of your Job With ' + client + ' is Due Tomorrow!'
                body = 'Hello ' + manager + ', you are more than halfway done with your job with, ' + manager + '. Be sure to email us at iblinkcompany@gmail.com to update us on any problems you are having. '
            else:
                subject = 'Your Third Milestone of your Job With ' + client + ' is Due Today!'
                body = 'Hey ' + manager + ', your third milestone of your job with , ' + manager + ' is due. Be sure to email us at iblinkcompany@gmail.com to update us on any problems you are having. '
        
        elif milestoneState == 4:
            if warning == True:
                subject = 'Your Fourth and Final Milestone of your Job With ' + client + ' is Due Tomorrow!'
                body = 'Hello ' + manager + ', you are more than halfway done with your job with, ' + manager + '. Be sure to email us at iblinkcompany@gmail.com to update us on any problems you are having. '
            else:
                subject = 'Your last milestone with ' + client + ' is due'
                body = 'Hello ' + manager + ', your job with, ' + manager + ' will be completed today. Make sure to long into your iBlinkco account to finish your fourth milestone if you have not. '

        if job_obj.length == 3:
            if milestoneState == 3:
                if warning == True:
                    subject = 'Your Third and Final Milestone of your Job With ' + client + ' is Due Tomorrow!'
                    body = 'Hello ' + manager + ', you are more than halfway done with your job with, ' + manager + '. Be sure to email us at iblinkcompany@gmail.com to update us on any problems you are having. '
                else:
                    subject = 'Your last milestone with ' + client + ' is due today'
                    body = 'Hello ' + manager + ', your job with, ' + manager + ' will be completed today. Make sure to long into your iBlinkco account to finish your third milestone if you have not. '
     
       # Sending emails
        email = EmailMessage(
            subject, body, to=[f'{manager_email}'])
        print(email)
        email.send()
        print({email})
        
    except Exception as e:
        print(e)
        

# Task to send rate job email
@shared_task
def rateJobEmail(manager, client, client_email):

    subject = "Rate" + manager + "'s job now"
    body = "Hello " + client + ", your job with " + manager +  " is complete. Rate there job here and let us know how your experience with iBlinkco is going be emailing us at iblinkcompany@gmail.com "

    # Sending emails
    email = EmailMessage(
        subject, body, to=[f'{client_email}'])
    print(email)
    email.send()

    print({email})
