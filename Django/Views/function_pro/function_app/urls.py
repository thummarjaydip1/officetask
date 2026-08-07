from django.urls import path
from function_app import views

urlpatterns = [
    path('', views.home, name="home"),
    path('add/', views.add_student, name="add"),
    path('display/', views.display_student, name="display"),
    path('update/<int:id>', views.update_student, name="update"),
    path('delete/<int:id>', views.delete_student, name="delete"),
]
