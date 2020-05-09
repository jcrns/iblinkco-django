import django
django.setup() 

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


# Creating manager assignement function
@periodic_task(run_every=(crontab(minute='*/20')), ignore_result=True)
def manager_assignment():

    # Getting unassigned jobs
    unassigned_jobs = JobPost.objects.filter(manager=None)
    print(unassigned_jobs)

    if not unassigned_jobs:
        print('ha')
    
    # Looping through all the jobs
    for job in unassigned_jobs:
        print('job')
        print(job)

        # Getting capable managers with filter
        managers = Profile.objects.filter(is_manager=True, language=client.profile.language, stripe_user_id=not None)
        
        if not managers:

            # Getting specific job
            current_job = JobPost.objects.get(pk=job.id)

            # Creating var to store
            selected_manager = None

            # Looping through managers
            for manager in managers:

                 # Randomly selecting managers
                manager_name = random.choice(managers)

                # Getting manager user
                manager = User.objects.get(username=manager_name)

                # Assigning manager
                selected_manager = manager
                
                # Ending loop
                break

            # Checking if manager was selected
            if selected_manager:

                # Emailing manager about job
                email = emailJobOffer(selected_manager, job_obj, current_site)

            else:
                print('manager not found')

    # Returning none
    return None

# # Creating func to look for manager every five minutes
# @periodic_task(run_every=(crontab(minute='*/20')), ignore_result=True)
# def manager_assignment(pk, current_site):
#     print('dfdfdfdfdf')

#     # Checking if we can retrieve job else returning
#     try:
#         job_obj = JobPost.objects.get(pk=pk)
#         print('sdsffafdvefge')

#         # Checking if job is none else returning
#         if not job_obj:
#             revoke('webapp.tasks.manager_assignment')
#             return None

#     except Exception as e:
#         print(e)
#         print('e')
#         revoke('webapp.tasks.manager_assignment')
#         return None

#     # Trying to get and assign manager and send email
#     try:
#         # Checking if manager already assigned if so returning
#         if job_obj.manager:
#             revoke('webapp.tasks.manager_assignment')
#             return None

#         # Getting client
#         client_name = job_obj.client
#         client = User.objects.get(username=client_name)

#         # Getting capable managers with filter
#         managers = Profile.objects.filter(
#             is_manager=True, language=client.profile.language, stripe_user_id=not None)

#         selected_manager = None
#         for manager in managers:
#             # Randomly selecting managers
#             manager_name = random.choice(managers)

#             # Getting manager user
#             manager = User.objects.get(username=manager_name)

#             # Checking if user has stripe connected
#             if not manager.profile.stripe_user_id:
#                 print("manager.profile.stripe_user_id")
#                 print(manager.profile.stripe_user_id)
#                 break
#             selected_manager = manager
        
#         # Checking if manager was selected
#         if selected_manager:
#             # Emailing manager about job
#             email = emailJobOffer(manager, job_obj, current_site)

#             print('complete')

#             revoke('webapp.tasks.manager_assignment')
#         else:
#             print('manager not found')
#         return None

#     except Exception as e:
#         print("e")
#         print(e)


# Creating main milestone email task
@shared_task
def milestone_send_emails(pk, milestoneState, warning):
    try:
        job_obj = JobPost.objects.get(pk=pk)
        print('sdsffafdvefge')

        # Checking if job is none else returning
        if not job_obj:
            revoke('webapp.tasks.milestone_send_emails')
            return None

    except Exception as e:
        print(e)
        revoke('webapp.tasks.milestone_send_emails')
        return None
    print('milestones')

    # Sending email to client
    check_milestone_client_email(job_obj, milestoneState)

    # Sending email to manager  
    milestone_manger_email(job_obj, milestoneState, warning)
    return None


# Alert milestone email clients
def check_milestone_client_email(job_obj, milestone):

    # Check if job still exist if not returning
    try:

        # Getting client and manager for email
        manager = job_obj.manager
        manager = User.objects.get(username=manager)
        manager = manager.username
        client = job_obj.client

        # Getting client emails
        client = User.objects.get(username=client)
        client_email = client.email
        client = client.username

        # Creating str variables
        if milestone == 1:
            milestone = 'One'
            body = 'Hello ' + client + ', We hope all is well, go to iblinkco.com to see rate ' + manager + ' job so far? Make sure to let us know by contacting us at iblinkcompany@gmail.com'

        elif milestone == 2:
            milestone = 'Two'
            body = 'Hey ' + client + ', your manager, ' + manager + ' second milestone is has been updated. Go to iblinkco.com to see it. If you have any questions email us at iblinkcompany@gmail.com. '

        elif milestone == 3:
            milestone = 'Three'
            body = 'Hello ' + client + ', you are more than halfway done with your job with, ' + manager + ' and they have just updated their third milestone. Be sure to email us at iblinkcompany@gmail.com to update us on any problems you are having. '

        elif milestone == 4:
            milestone = 'Four'
            body = 'Hello ' + client + ', your job with, ' + manager + ' has been completed. Make sure to long into your iBlinkco account now to see the work they have done and to give your final rating on their job.  '

        # Sending emails
        if job.length == 3:
            if milestone == 3:
                milestone = 'Third'
                body = 'Hello ' + client + ', your job with, ' + manager + ' has been completed. Make sure to long into your iBlinkco account now to see the work they have done and to give your final rating on their job.  '
        # Client email
        email = EmailMessage(
            'Milestone ' + milestone + ' Check In and Rate', body, to=[f'{client_email}'])
        print(email)
        email.send()
        print({email})

        return None
    except Exception as e:
        print(e)
        return None

# Alert milestone email managers
def milestone_manger_email(job_obj, milestoneState, warning):
    print('dfdfdfdfdf')

    # Checking if we can retrieve job else returning
    try:
        # Getting client and manager for email
        manager = job_obj.manager

        client = job_obj.client
        client = User.objects.get(username=client)
        client = client.username
        
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
                body = 'Hello ' + manager + ', We hope all is well, How is your job with ' + client + \
                    ' going so far? Make sure to update your first milestone by tomorrow. If you have any questions, contact us at iblinkcompany@gmail.com'

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
    body = "Hello " + client + ", your job with " + manager + \
        " is complete. Rate there job here and let us know how your experience with iBlinkco is going be emailing us at iblinkcompany@gmail.com "

    # Sending emails
    email = EmailMessage(
        subject, body, to=[f'{client_email}'])
    print(email)
    email.send()

    print({email})

# Task to notify manager about milestone being rated
@shared_task
def milestoneRatedEmail(manager, client, manager_email, milestone_number, star_count):

    # Checking what number
    if milestone_number == 1:
        milestone_number = 'one'
    elif milestone_number == 2:
        milestone_number = 'two'
    elif milestone_number == 3:
        milestone_number = 'three'
    elif milestone_number == 4:
        milestone_number = 'four'

    subject = client + " has rated your job during milestone " + str(milestone_number) + " " + str(star_count) + " stars"
    
    if star_count == 5:
        greatness_of_job = " seems to be going great! They gave you " + str(star_count) + " on your last milestone."
    elif star_count == 4:
        greatness_of_job = " seems to be going good. They gave you " + str(star_count) + " on your last milestone which means they like the job but maybe you can do better."
    elif star_count == 3:
        greatness_of_job = " is tolerable. They gave you " + str(star_count) + " on your last milestone. We encourage you step up for the next milestone to avoid having your overall rating significantly penalized."
    elif star_count < 3:
        greatness_of_job = " wasn't as good as they expected. They gave you " + str(star_count) + " on your last milestone. We encourage you step up for the next milestone to avoid having your overall rating significantly penalized. Too many low stars on your accounts can get your account disabled."

    ending = " If you have any questions or concerns email us at iblinkcompany@gmail.com"
    body = "Hello " + manager + ", your job with " + client + greatness_of_job + ending

    # Sending emails
    email = EmailMessage(
        subject, body, to=[f'{manager_email}'])
    print(email)
    email.send()

    print({email})
    return 'success'


@shared_task
def jobPrepEndedEmail(manager, client, client_email):

    subject = 'Job preparation period ended. ' + manager + ' will start working on your job.'
    body = "Hello " + client + ", " + manager + " has ended their job preperation period and is starting to work on your requested services."

    # Sending email to client
    email = EmailMessage(
        subject, body, to=[f'{client_email}'])
    print(email)
    email.send()


manager_assignment()
