from django.urls import path

from . import views

urlpatterns = [
    path('users/', views.UserRegistrationView.as_view(), name='user_registration'),
    path('users/login/', views.LoginView.as_view(), name='user_login'),
    path('secured-data', views.SensitiveDataView.as_view(), name='secured_data'),
    ]
