from django.urls import path
from students import views

urlpatterns = [
    path("", views.display_student, name="display"),
    path("add/", views.add_student, name="add"),
    path("detail/<int:id>/", views.detail_student, name="detail"),
    path("update/<int:id>/", views.update_student, name="update"),
    path("delete/<int:id>/", views.delete_student, name="delete"),
]
