from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Personal data
    first_name = models.CharField(max_length=60, default='none')
    last_name = models.CharField(max_length=60, default='none')
    language = models.CharField(max_length=60, default='none')
    date_of_birth = models.DateTimeField(verbose_name='date of birth', auto_now_add=True)

    # Bool for if user is currently in a job
    busy = models.BooleanField(default=False)

    # type of profile
    is_manager = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    # Business data 
    business_name = models.CharField(max_length=60, default='none')
    business_type = models.CharField(max_length=60, default='none')
    business_description = models.TextField(max_length=350, default='none')

    # Other information
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):
    #     super().save()

    #     # Getting img
    #     img = Image.open(self.image.path)

    #     # Resizing img
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)