from django.urls import path

from . import views

urlpatterns = [
    path('integration/', views.GetIntegrationJson.as_view(), name='integration_json'),
    path('tick/', views.Tick.as_view(), name='tick'),
    ]
