from django.urls import path
from app1 import views

urlpatterns = [
    path('create/',views.create_student),
    path('update/',views.updated_student),
    path('delete/',views.delete_student)
]
