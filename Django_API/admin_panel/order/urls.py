from django.urls import path, include
from .views import *
from order import views

urlpatterns = [
    path("order_now/<int:id>/", views.order_now, name="order_now"),
    path("order_display/", views.order_display, name="order_display"),
    path("order_user_edit/<int:id>/", views.order_user_edit, name="order_user_edit"),
    path(
        "order_user_delete_table/<int:id>/",
        views.order_user_delete_table,
        name="order_user_delete_table",
    ),
    path("order_history/<int:id>/", views.order_history, name="order_history"),
    path("bill/<int:id>/", views.bill_system, name="bill_system"),
    path("pdf_download/<int:id>/", views.pdf_download, name="pdf_download"),
]
