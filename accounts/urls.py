from django.urls import path
from .views import user_logout, create_user_account, manage_users
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('login/', user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('manage_users/', manage_users, name='manage_users'),
    path('create_user/', create_user_account, name='create_user'),
]