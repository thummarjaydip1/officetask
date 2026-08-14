from django.urls import path
from users import views

urlpatterns = [
    path("add_user/", views.add_user, name="add_user"),
    path("list_user/", views.list_user, name="list_user"),
    path("update_user/<int:id>", views.update_user, name="update_user"),
    path("delete_user/<int:id>", views.delete_user, name="delete_user"),
]
