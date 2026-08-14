from django.urls import path
from shop import views

urlpatterns = [
    path("", views.index, name="index"),

    path("auth_register/", views.auth_register, name="auth_register"),
    path("auth_login/", views.auth_login, name="auth_login"),
    path("auth_logout/", views.auth_logout, name="auth_logout"),
    path("user_profile/", views.user_profile, name="user_profile"),
    path("update_profile/", views.update_profile, name="update_profile"),
    path("delete_user/", views.delete_user, name="delete_user"),
    path("user_list/", views.user_list, name="user_list"),

    path("add_product/", views.add_product, name="add_product"),
    path("list_product/", views.list_product, name="list_product"),
    path("product_detail/<int:id>/", views.product_detail, name="product_detail"),
    path("update_product/<int:id>/", views.update_product, name="update_product"),
    path("delete_product/<int:id>/", views.delete_product, name="delete_product"),

    path("order_now/<int:id>/", views.order_now, name="order_now"),
    path("user_order/", views.user_order, name="user_order"),
    path("order_detail/<int:id>/", views.order_detail, name="order_detail"),
    path("update_order/<int:id>/", views.update_order, name="update_order"),
    path("delete_order/<int:id>/", views.delete_order, name="delete_order"),
]
