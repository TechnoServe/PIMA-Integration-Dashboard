from django.urls import path
from .views import user_logout, create_user_account, manage_users, delete_user, edit_user, password_reset_request
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('login/', user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('manage_users/', manage_users, name='manage_users'),
    path('create_user/', create_user_account, name='create_user'),
    path('edit_user/<int:id>/', edit_user, name='edit_user'),
    path('delete_user/<int:id>/', delete_user, name='delete_user'),

    #PASSWORD RESET
    path('password_reset/', password_reset_request, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html') , name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html") , name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html')  , name='password_reset_complete'),
]