from django.urls import path
from temp_app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('filter/', views.filter_page, name="filter"),
    path("boolean_operator/", views.boolean_operator, name="boolean_operator"),
    path("for_loop/", views.for_loop_temp, name="for_loop"),
    path("if_else/", views.if_else_temp, name="if_else")
]
