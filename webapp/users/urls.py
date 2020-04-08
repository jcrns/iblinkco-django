from django.urls import path
from django.contrib.auth import views as auth_views

from . import views 

urlpatterns = [
    # User functions
    path('signup', views.registerFunc, name='users-signup'),
    path('login', views.loginFunc, name='users-login'),
    path('logout', views.logoutFunc, name='users-logout'),
    # Profile functions
    path('confirm_user', views.comfirmUser, name='users-confirm-user-type'),

]