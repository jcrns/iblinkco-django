from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    is_manager = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# #User Accounts
# class MyAcccountManager(BaseUserManager):
#     def create_user(self, email, username, password=None):
#         if not email:
#             raise ValueError("Users most have an email")
#         if not username:
#             raise ValueError("Users most have a username")
#         user = self.model(
#             email = self.normalize_email(email),
#             username=username,
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
#     def create_superuser(self, email, username, password):
#         user = self.model(
#             email = self.normalize_email(email),
#             password=password,
#             username=username,
#         )
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user
# # Account paramaters
# class account(AbstractBaseUser):
#     email = models.EmailField(verbose_name='email', max_length=60, unique=True)
#     username = models.CharField(max_length=60, unique=True)
#     date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
#     last_login = models.DateTimeField(verbose_name='last login', auto_now_add=True)
#     is_admin = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     is_manager = models.BooleanField(default=False)
#     is_client = models.BooleanField(default=False)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["username",]

#     def __str__(self):
#         return self.username

#     objects = MyAcccountManager()

#     def has_perm(self, perm, obj=None):
#         return self.is_admin

#     def has_module_perms(self, app_label):
#         return True

