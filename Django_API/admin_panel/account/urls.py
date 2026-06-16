from django.urls import path, include
from .views import *
from account import views

urlpatterns = [
    path("auth_login/", views.auth_login, name="auth_login"),
    path("auth_register/", views.auth_register, name="auth_register"),
    path(
        "auth_forget_password/", views.auth_forget_password, name="auth_forget_password"
    ),
    path("auth_logout/", views.auth_logout, name="auth_logout"),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path("auth_profile/", views.auth_profile, name="auth_profile"),
    path("auth_profile_edit/", views.auth_profile_edit, name="auth_profile_edit"),
]
