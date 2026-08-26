from django.urls import path
from auth_app import views
from .views import *


urlpatterns = [
    path('register-user/', views.register_user),
    path("get-user/", views.get_user),
    path("update-user/<int:id>", views.update_user),
    path("delete-user/<int:id>", views.delete_update),
    path("login-user/", LoginAPIView.as_view()),
]
