from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from .choices import * 

class JobPost(models.Model):
    # Users involved
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client', null=True)
    manager = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='manager')

    # Job Length
    number_of_post = models.IntegerField()
    length = models.IntegerField()
    
    # Paying
    price_paid = models.FloatField(null=True)
    paid_for = models.IntegerField(default=False)

    # Job Details
    job_complete = models.BooleanField(default=False)
    captions = models.BooleanField(default=False)
    search_for_content = models.BooleanField(default=False)
    post_for_you = models.BooleanField(default=False)
    engagement = models.BooleanField(default=False)
    service_description = models.CharField(max_length=1000, default='none')
    manager_randomly_assigned = models.BooleanField(default=True)

    # Platforms
    instagram = models.BooleanField(default=False)
    facebook = models.BooleanField(default=False)

    # Platform Username
    instagram_username = models.CharField(max_length=100, blank=True, default='none')
    facebook_username = models.CharField(max_length=100, blank=True, default='none')

    # Milestone
    completed_milestone_one = models.BooleanField(default=False)
    milestone_one_statement = models.CharField(max_length=1000, default='none')

    completed_milestone_two = models.BooleanField(default=False)
    milestone_two_statement = models.CharField(max_length=1000, default='none')
    
    completed_milestone_three = models.BooleanField(default=False)
    milestone_three_statement = models.CharField(max_length=1000, default='none')
    
    completed_milestone_four = models.BooleanField(default=False)
    milestone_four_statement = models.CharField(max_length=1000, default='none')

    # Date Job Posted
    date_requested = models.DateTimeField(verbose_name='date requested', auto_now_add=True)

    def __str__(self):
        return f'{self.client} Job Request {self.date_requested}'
