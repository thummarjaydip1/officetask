from django.urls import path
from books import views

urlpatterns = [
    path("", views.list_book , name="list"),
    path("add/", views.add_book , name="add"),
    path("detail/<int:id>/", views.detail_book , name="detail"),
    path("update/<int:id>/", views.update_book , name="update"),
    path("delete/<int:id>/", views.delete_book , name="delete"),
]
