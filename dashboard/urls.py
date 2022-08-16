from django.urls import path
from .views import project_list

urlpatterns = [
    path('projectlist/', project_list, name='project_list'),
]