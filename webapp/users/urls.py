from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signUp, name='users-signup'),
    path('login', views.login, name='users-login'),
]