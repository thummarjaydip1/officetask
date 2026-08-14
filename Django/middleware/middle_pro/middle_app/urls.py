from django.urls import path 
from middle_app import views

urlpatterns = [
    path('', views.index, name="index")
]
