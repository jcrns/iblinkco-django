from django.db import models

# Importing to configure before save
from django.db.models.signals import pre_save

from django.contrib.auth.models import User
from .choices import * 
import datetime

# Importing to create job id
from webapp.utils import random_string_generator

class JobPost(models.Model):

    # JOB ID
    job_id = models.CharField(max_length=120, blank=True)
    
    # Users involved
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client', null=True)
    manager = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='manager', blank=True)

    # Job Length
    number_of_post = models.IntegerField()
    length = models.IntegerField()
    
    # Paying
    manager_payment = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    price_paid = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    paid_for = models.BooleanField(default=False)
    job_fee = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    manager_paid = models.BooleanField(default=False)

    # Job Details
    job_complete = models.BooleanField(default=False)
    captions = models.BooleanField(default=False)
    search_for_content = models.BooleanField(default=False)
    post_for_you = models.BooleanField(default=False)
    engagement = models.BooleanField(default=False)
    service_description = models.CharField(max_length=5000, default='none')
    manager_randomly_assigned = models.BooleanField(default=True)

    # Platforms
    instagram = models.BooleanField(default=False)
    facebook = models.BooleanField(default=False)

    # Platform Username
    instagram_username = models.CharField(max_length=100, blank=True, default='none')
    facebook_username = models.CharField(max_length=100, blank=True, default='none')

    # Milestones
    completed_milestone_one = models.BooleanField(default=False)
    milestone_one_statement = models.CharField(max_length=1000, default='none')
    milestone_one_files = models.FileField(default='default.jpg',  upload_to='milestone_files')

    completed_milestone_two = models.BooleanField(default=False)
    milestone_two_statement = models.CharField(max_length=1000, default='none')
    milestone_two_files = models.FileField(default='default.jpg',  upload_to='milestone_files')

    completed_milestone_three = models.BooleanField(default=False)
    milestone_three_statement = models.CharField(max_length=1000, default='none')
    milestone_three_files = models.FileField(default='default.jpg', upload_to='milestone_files')


    completed_milestone_four = models.BooleanField(default=False)
    milestone_four_statement = models.CharField(max_length=1000, default='none')
    milestone_four_files = models.FileField(default='default.jpg',  upload_to='milestone_files')

    # Job Preparation
    job_preparation_completed = models.BooleanField(default=False)
    job_preparation_deadline = models.DateTimeField(
        max_length=8, blank=True, null=True)

    # Date Job Posted
    date_requested = models.DateTimeField(
        verbose_name='date requested', auto_now_add=True)

    # Deadline for job
    deadline = models.DateTimeField(max_length=8, blank=True, null=True)

    def __str__(self):
        print(self.manager)
        return f'{self.client} Job Request {self.job_id}'

    # Overriding the save function to check if manager was assigned
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.manager != None:
            
            # Creating deadline for job
            now = datetime.date.today()
            print('current time', now)

            # Getting absolute job length by adding regular job length and preparation time
            realJobLength = self.length + 2

            # Adding the absolute job length to current time
            deadline = now + datetime.timedelta(days=realJobLength)
            print('new deadline', deadline)
            self.deadline = deadline

            # Getting preparation time
            now = now + datetime.timedelta(days=2)
            self.job_preparation_deadline = now

        super(JobPost, self).save(force_insert, force_update, *args, **kwargs)

def pre_save_create_job_id(sender, instance, *args, **kwargs):
    if not instance.job_id:
        instance.job_id = random_string_generator(size=16)

pre_save.connect(pre_save_create_job_id, sender=JobPost)

# Milestone file model
class MilestoneFiles(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    milestoneOne = models.BooleanField(default=False)
    milestoneTwo = models.BooleanField(default=False)
    milestoneThree = models.BooleanField(default=False)
    milestoneFour = models.BooleanField(default=False)
    milestoneFile = models.FileField()
