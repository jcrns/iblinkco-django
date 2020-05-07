from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django_resized import ResizedImageField
from django.core.mail import EmailMessage
from django.db.models.signals import pre_save
from django.dispatch import receiver

class ManagerEvaluation(models.Model):
    # Manager
    manager = models.OneToOneField(User, on_delete=models.CASCADE)

    # Checking if evaluation was started 
    evaluation_started = models.BooleanField(default=False)
    
    # Checking if manager was accepted and creating prevalue to see if it is changed
    accepted = models.BooleanField(default=False)
    __original_accepted = None

    # Checking if evaluation was completed
    evaluation_completed = models.BooleanField(default=False)

    # Question one answer 
    answer_one_caption_one = models.TextField(max_length=2200, default='none')
    answer_one_caption_two = models.TextField(max_length=2200, default='none')
    answer_one_caption_three = models.TextField(max_length=2200, default='none')
    
    # sample answer
    # 1. ....
    # 2 ...

    # Question two answer 
    answer_two_caption = models.TextField(max_length=2200, default='none')
    answer_two_what_are_problems = models.TextField(max_length=2200, default='none')
    answer_two_img = models.ImageField(default='default.jpg', upload_to='application_pics')

    # Question three answer
    answer_three_caption = models.TextField(max_length=2200, default='none')
    answer_three_img = models.ImageField(default='default.jpg', upload_to='application_pics')

    # Question four answer
    choose_job = models.BooleanField(default=False)

    # Overriding init func
    def __init__(self, *args, **kwargs):
        super(ManagerEvaluation, self).__init__(*args, **kwargs)
        self.__original_accepted = self.accepted

    # # Overriding save func
    # def save(self, force_insert=False, force_update=False, *args, **kwargs):
    #     print("self.__original_accepted")
    #     print(self.__original_accepted)
    #     print(self.accepted)
    #     # Check if user has changed
    #     if self.__original_accepted != self.accepted:
    #         if self.accepted == True:
    #             # Sending Email if user was accepted
    #             self.managerAccepted()
    #     super(ManagerEvaluation, self).save(force_insert, force_update, *args, **kwargs)
    #     self.__original_accepted = self.accepted

    def __str__(self):
        return f'{self.manager} Evaluation'
    
    # Email manager accepted


    def managerAccepted(self):
        user = self.manager
        # Getting current site
        mail_subject = 'Congratulations ' + user.username + ' You Have Been Verified for iBlinkco'

        # Creating message body and rendering from template
        messageBody = 'You are now able to conduct social media management services for clients on iblinkco.com. Be sure to consistently check your email as we will let you know when you have been assigned to a job.'

        # Getting email
        email = user.email

        print(email)

        # Sending email
        email = EmailMessage(mail_subject, messageBody, to=[f'{email}'])
        email.send()
        return email

# Checking if acceptance has changed
@receiver(pre_save, sender=ManagerEvaluation)
def manager_acceptance(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # Object is new, so field hasn't technically changed, but you may want to do something else here.
        pass
    else:
        if not obj.accepted == instance.accepted:  # Field has changed
            if instance.accepted == True:
                # Sending Email if user was accepted
                ManagerEvaluation.managerAccepted(instance)
