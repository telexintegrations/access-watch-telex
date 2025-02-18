from django.urls import path

from . import views

urlpatterns = path('users/', views.UserRegistrationView.as_view(), name='user_registration'),
