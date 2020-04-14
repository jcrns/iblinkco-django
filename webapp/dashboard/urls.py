from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard-home'),
    path('job-details/<int:pk>/', views.JobDetailView.as_view(), name='dashboard-job-detail'),
]
