from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard_map, name='dashboard_map'),
]