from django.urls import path
from . import views

urlpatterns = [
    path('evaluation', views.evaluation, name='management-evaluation'),
    path('authorize_stripe', views.stripeAuthorizeView,
         name='management-authorize-stripe'),
    path('users/oauth/callback/', views.stripeAuthorizeCallbackView,
         name='management-authorize-callback'),

]
