from django.urls import path
from app1 import views

urlpatterns = [
    path('',views.add_data,name="add_data"),
    path('display/',views.display_data,name="display"),
]
