from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage-home'),
    path('terms_and_conditions', views.termsAndConditions, name='homepage-terms-and-conditions'),
    path('privacy_policy', views.privacyPolicy, name='homepage-privacy-policy'),
    path('become_a_manager', views.becomeManager, name='homepage-become-a-manager'),
]
