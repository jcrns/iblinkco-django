from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django_resized import ResizedImageField

class ManagerEvaluation(models.Model):
    # Manager
    manager = models.OneToOneField(User, on_delete=models.CASCADE)

    # Checking if evaluation was started
    evaluation_started = models.BooleanField(default=False)

    # Checking if manager was accepted
    accepted = models.BooleanField(default=False)

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

    def __str__(self):
        return f'{self.manager} Evaluation'