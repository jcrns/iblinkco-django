from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# User Registration Form
class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        # Fields user needs to sign up
        fields = ['username', 'email', 'password1', 'password2']
    
        # creating custom form by importing UserRegisterForm and adding custom fields
    def getemail(self):
        email = forms.EmailField()

# Creating form for complete profile page
class ProfileUpdateForm(forms.ModelForm):
    businessTypeChoices = (('Services', 'Services'), ('Retail', 'Retail'), ('Art & Entertainment', 'Art & Entertainment'), ('Tech', 'Tech'), ('Events', 'Events'), ('Farming6', 'Farming'), ('Health Care', 'Health Care'), ('Restaurants', 'Restaurants'), ('Other', 'Other'))
    first_name = forms.CharField(label='First Name',widget=forms.TextInput(attrs={'placeholder':'Enter', 'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name',widget=forms.TextInput(attrs={'placeholder':'Enter', 'class': 'form-control'}))
    language = forms.CharField(label='Language',widget=forms.TextInput(attrs={'placeholder':'Enter', 'class': 'form-control'}))
    business_name = forms.CharField(label='Business Name',widget=forms.TextInput(attrs={'placeholder':'Enter', 'class': 'form-control'}))
    business_type = forms.ChoiceField(label='Business Type',choices=businessTypeChoices, widget=forms.Select(attrs={ 'class': 'form-control' }))
    business_description = forms.CharField(label='Business Description',widget=forms.Textarea(attrs={'placeholder':'Enter ...', 'rows' : '5', 'class' : 'form-control' }))
    # image = forms.FileField(label='Image')

    class Meta:
        model = Profile
        fields = ["first_name", "language", "last_name", "business_name", "business_type", "business_description", "image"]