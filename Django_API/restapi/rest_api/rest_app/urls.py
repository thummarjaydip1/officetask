from django.urls import path
from rest_app import views
from .views import *

urlpatterns = [
    path("add/",views.add_student),
    path("display/",views.display_student),
    path("profile/<int:id>/",views.student_profile),
    path("update/<int:id>/",views.update_student),
    path("delete/<int:id>/",views.delete_student),
    path("search/",views.search_student),
    path("filter/",views.filter_student),
    path("count/",count_student)
]