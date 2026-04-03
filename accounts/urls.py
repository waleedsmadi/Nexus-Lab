from django.urls import path
from . import views


app_name='accounts'

urlpatterns = [
    path('login/', views.login_view, name='login_view_url'),
    path('logout/', views.logout_account, name='logout_account_url'),
    path('signup/', views.signup_view, name='signup_view_url'),
    path('activation/', views.activation_account, name='activation_message_url'),
    path('activation-error-message/', views.activation_error_message, name='activation_error_message_url'),
    path('resend-activation-link/', views.resend_activation_link, name='resend_activation_link_url'),
    path('reset-password/check-email/', views.check_email, name='check_email_url'),
    path('edit-profile/<str:username>/', views.profile, name="profile_view_url"),
    path('change_password/<str:username>/', views.change_password, name="change_password_url"),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password_url'),
    path('<str:uid>/<str:token>/', views.activation_account_link, name='activation_account_link_url'),
]
