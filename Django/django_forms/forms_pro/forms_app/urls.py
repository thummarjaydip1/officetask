from django.urls import path
from forms_app import views

urlpatterns = [
    path("student/", views.student_form),
    path("feedback/", views.feedback_form),
    path("contact/", views.contact_form),
    path("person/", views.person_form),
    path("book/", views.book_form),
]
