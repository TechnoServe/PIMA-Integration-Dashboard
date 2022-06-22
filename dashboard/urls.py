from django.urls import path
from .views import dummy_map

urlpatterns = [
    path('', dummy_map, name='dummy_map'),
]