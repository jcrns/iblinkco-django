from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# User Registration Form
class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        # Fields user needs to sign up
        fields = ['username', 'email', 'password1', 'password2']
    
        # creating custom form by importing UserRegisterForm and adding custom fields
    def getemail(self):
        email = forms.EmailField()