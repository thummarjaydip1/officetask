from django.urls import path
from cache_app import views

urlpatterns = [
    path('', views.list_student)
]