from django.urls import path
from .views import dummy_map, exported

urlpatterns = [
    path('dummy/', dummy_map, name='dummy_map'),
    path('exported/', exported, name='exported'),
]