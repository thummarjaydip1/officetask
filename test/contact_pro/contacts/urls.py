from django.urls import path
from contacts import views

urlpatterns = [
    path('', views.list_contact, name="list_contact"),

    path('add_contact/', views.add_contact, name="add_contact"),

    path('update_contact/<int:id>/', views.update_contact, name="update_contact"),

    path('detail_contact/<int:id>/', views.detail_contact, name="detail_contact"),

    path('delete_contact/<int:id>/', views.delete_contact, name="delete_contact"),

    path('add_phonenum', views.add_phonenum, name="add_phonenum"),

    path('update_phonenum/<int:id>/', views.update_phonenum, name="update_phonenum"),

    path('delete_phonenum/<int:id>/', views.delete_phonenum, name="delete_phonenum"),
]
