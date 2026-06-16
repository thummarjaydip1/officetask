from django.urls import path, include
from .views import *
from rest_app import views

urlpatterns = [
    path("add/", views.add_student),
    path("display/", views.display_student),
    path("update/<int:id>/", views.update_student),
    path("delete/<int:id>/", views.delete_student),
]
