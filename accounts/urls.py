from django.urls import path
from .views import user_logout, create_user_account, manage_users, delete_user, edit_user
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('login/', user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('manage_users/', manage_users, name='manage_users'),
    path('create_user/', create_user_account, name='create_user'),
    path('edit_user/<int:id>/', edit_user, name='edit_user'),
    path('delete_user/<int:id>/', delete_user, name='delete_user'),
]