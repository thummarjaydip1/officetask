from django.urls import path
from query_app import views

urlpatterns = [
    path('',views.home)
]
