from django.urls import path, include
from management import views
from rest_framework import routers
from .views import *

urlpatterns = [
    # normal project url
    path("", views.index, name="index"),
    path("error_page/", views.error_page, name="error_page"),
    path("maintenance_page/", views.maintenance_page, name="maintenance_page"),
    path("tables/", views.tables, name="tables"),
    path("user_table_edit/<int:id>/", views.user_table_edit, name="user_table_edit"),
    path(
        "user_table_delete/<int:id>/", views.user_table_delete, name="user_table_delete"
    ),
    path(
        "order_admin_edit_table/<int:id>/",
        views.order_admin_edit_table,
        name="order_admin_edit_table",
    ),
    path(
        "order_admin_delete_table/<int:id>/",
        views.order_admin_delete_table,
        name="order_admin_delete_table",
    ),
    path("news/", views.news, name="news"),
    path("documentation/", views.documentation, name="documentation"),
]
