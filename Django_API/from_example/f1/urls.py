from django.urls import path
from .views import *
from f1 import views

urlpatterns = [
    path('',views.home,name="home"),
    path('contact/',views.contact_add,name="contact"),
    path('contact_update/<int:id>/',views.contact_update,name="contact_update"),
    path('contact_delete/<int:id>/',views.contact_delete,name="contact_delete"),
    path('feedback/',views.feedback_add,name="feedback"),
    path('feedback_update/<int:id>/',views.feedback_update,name="feedback_update"),
    path('feedback_delete/<int:id>/',views.feedback_delete,name="feedback_delete"),

    path('student_list/',StudentListview.as_view(),name="student_list"),
    path('student_add/',StudentCreateView.as_view(),name="student_add"),
    path('student_update/<int:pk>/',StudentUpdateView.as_view(),name="student_update"),
    path('student_add/<int:pk>/',StudentDeleteView.as_view(),name="student_delete")
]
