from django.urls import path,include
from myapi import views
from rest_framework import routers
from .views import *

urlpatterns = [
    path('add-student/',add_student),
    path('get-student/',get_student),
    path('get-student-id/<int:id>/',get_student_id),
    path('update-student/<int:id>/',update_student),
    path('delete-student/<int:id>/',delete_student),

    path('student_add_data/',views.student_add_data,name="student_add_data"),
    path('student_display_data/',views.student_display_data,name="student_display_data"),
    path('student_update_data/<int:id>/',views.student_update_data,name="student_update_data"),
    path('student_delete_data/<int:id>/',views.student_delete_data,name="student_delete_data")
]