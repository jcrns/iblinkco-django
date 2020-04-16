from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard-home'),
    path('job-details/<int:pk>/', views.JobDetailView.as_view(), name='dashboard-job-detail'),
    path('confirm-job/<int:pk>/', views.ConfirmJobDetailView.as_view(), name='dashboard-confirm-job'),
    path('job-details/<int:pk>/delete/', views.deleteJob, name='dashboard-job-delete'),
]
