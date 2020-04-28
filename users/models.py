from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
now = date(2000, 1, 1) 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Personal data
    first_name = models.CharField(max_length=60, default='none')
    last_name = models.CharField(max_length=60, default='none')
    language = models.CharField(max_length=60, default='none')
    date_of_birth = models.DateField(max_length=8, blank=True, null=True)


    # Bool for if user is currently in a job
    busy = models.BooleanField(default=False)

    # type of profile
    is_manager = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    # Business data 
    business_name = models.CharField(max_length=60, default='none')
    business_type = models.CharField(max_length=60, default='none')
    description = models.TextField(max_length=500, default='none')

    # Other information
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)

    # Checking if user is fully verified
    image = models.ImageField(default='profile-blank.png', upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    # def save(self, *args, **kwargs):
    #     if self.image:
    #         self.image = get_thumbnail(self.image, '300x300', quality=99, format='JPEG')
    #     super(Profile, self).save(*args, **kwargs)