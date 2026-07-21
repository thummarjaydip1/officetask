from django.urls import path,include
from .views import *
from app1 import views

urlpatterns = [
    # api urls
    path("register_api/",views.register_api,name="regiter_api"),
    path("login_api/",views.login_api,name="login_api"),
    path("logout_api/",views.logout_api,name="logout_api"),
    path("user_display_api/",views.user_display_api,name="user_display_api"),
    path("user_display_id_api/<int:id>/",views.user_display_id_api,name="user_display_id_api"),
    path("user_update_api/<int:id>/",views.user_update_api,name="user_display_api"),
    path("user_delete_api/<int:id>/",views.user_delete_api,name="user_delete_api"),

    # pages url
    path("",views.index,name="index"),
    path("register/",views.auth_register,name="register"),
    path("login/",views.auth_login,name="login"),
    path("logout/",views.auth_logout,name="logout"),
    path("user_update/<int:id>/",views.user_update,name="user_update"),
    path("user_delete/<int:id>/",views.user_delete,name="user_delete"),

    path("profile/",views.profile,name="profile"),
]
