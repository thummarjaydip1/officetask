from django.urls import path
from cart import views

urlpatterns = [
    path("add_to_cart/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path("user_cart/", views.user_cart, name="user_cart"),
    path("update_cart/<int:id>/", views.update_cart, name="update_cart"),
    path("delete_cart/<int:id>/", views.delete_cart, name="delete_cart"),
]
