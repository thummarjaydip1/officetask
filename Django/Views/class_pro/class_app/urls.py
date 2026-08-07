from django.urls import path
from .views import StudentCreate, StudentList, StudentUpdate, StudentDelete

urlpatterns = [
    path("", StudentList.as_view(), name="display"),
    path("add/", StudentCreate.as_view(), name="add"),
    path("update/<int:pk>", StudentUpdate.as_view(), name="update"),
    path("delete/<int:pk>", StudentDelete.as_view(), name="delete"),
]
