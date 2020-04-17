from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class ManagerEvaluation(models.Model):
    # Manager
    manager = models.OneToOneField(User, on_delete=models.CASCADE)

    # Checking if evaluation was started
    evaluation_started = models.BooleanField(default=False)

    # Question one answer 
    answer_one_caption_one = models.TextField(max_length=350, default='none')
    answer_one_caption_two = models.TextField(max_length=350, default='none')
    answer_one_caption_three = models.TextField(max_length=350, default='none')
    # sample answer
    # 1. ....
    # 2 ...

    # Question two answer 
    answer_two = models.TextField(max_length=350, default='none')
    answer_two_img = models.ImageField(upload_to='application_pics', null=True)

    # Question three answer
    answer_three = models.TextField(max_length=280, default='none')

    # Question four answer
    choose_job = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.manager} Evaluation'