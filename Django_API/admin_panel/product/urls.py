from django.urls import path, include
from .views import *
from product import views

urlpatterns = [
    # path('product_details/<int:id>',views.product_display,name="prooduct_details"),
    path("product_display/", views.product_display, name="product_display"),
    path(
        "product_display_id/<int:id>/",
        views.product_display_id,
        name="product_display_id",
    ),
    path("product-qr/<int:id>/", views.product_qr, name="product_qr"),
    path("form_category/", views.form_category, name="form_category"),
    path(
        "form_category_edit/<int:id>/",
        views.form_category_edit,
        name="form_category_edit",
    ),
    path(
        "form_category_delete/<int:id>/",
        views.form_category_delete,
        name="form_category_delete",
    ),
    path("form_product/", views.form_product, name="form_product"),
    path(
        "form_product_edit/<int:id>/", views.form_product_edit, name="form_product_edit"
    ),
    path(
        "form_product_delete/<int:id>/",
        views.form_product_delete,
        name="form_product_delete",
    ),
    path("add_wishlist/<int:id>/", views.add_wishlist, name="add_wishlist"),
    path("show_wishlist", views.show_wishlist, name="show_wishlist"),
    path("remove_wishlist/<int:id>/", views.remove_wishlist, name="remove_wishlist"),
]
