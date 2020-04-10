from django.urls import path
from . import views

urlpatterns = [
    path('post_a_job', views.postJob, name='service-job'),
    path('complete_profile', views.completeProfile, name='service-complete-profile'),
]
