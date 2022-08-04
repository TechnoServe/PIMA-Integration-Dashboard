from django.urls import path
from .views import project_list

urlpatterns = [
    path('projectlist/', project_list, name='project_list'),
    #path('exported/', exported, name='exported'),
    #path('observations/', salesforceObs, name='observations'),
]