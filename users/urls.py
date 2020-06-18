from django.urls import path
from django.contrib.auth import views as auth_views

from . import views 

urlpatterns = [
    # User functions
    path('signup', views.registerFunc, name='users-signup'),
    path('login', views.loginFunc, name='users-login'),
    path('logout', views.logoutFunc, name='users-logout'),
    path('activate/(P<uidb64>[0-9A-Za-z_\-]+)/(P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        views.activate, name='users-activate'),
    
    # Password reset and change
    # path('password_reset', auth_views.Pa, name='password_reset'),
    # path('password_reset/done/$', auth_views.password_reset_done,
    #     name='password_reset_done'),
    # path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     auth_views.password_reset_confirm, name='password_reset_confirm'),
    # path(r'^reset/done/$', auth_views.password_reset_complete,
    #     name='password_reset_complete'),

    # Profile functions
    path('confirm_user', views.comfirmUser, name='users-confirm-user-type'),
]
