from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.GetIntegrationJson.as_view(), name='integration_json'),
    path('tick/', views.Tick.as_view(), name='tick'),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)
