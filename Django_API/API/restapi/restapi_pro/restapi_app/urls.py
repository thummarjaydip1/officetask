from django.urls import path, include
from restapi_app import views

from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(f"contacts", ContactViewSet)

urlpatterns = [
    # Contact API urls
    path('api/',include(router.urls)),

    # Student API urls
    path("add-student/", views.add_student),
    path("get-student/", views.get_student),
    path("update-student/<int:id>/", views.update_student),
    path("delete-student/<int:id>/", views.delete_student),
    path("search-student/",views.search_student),

    # Feedback API urls
    path("add-feedback/", views.add_feedback),
    path("get-feedback/", views.get_feedback),
    path("update-feedback/<int:id>/", views.update_feedback),
    path("delete-feedback/<int:id>/", views.delete_feedback),
    path("search-feedback/", views.search_feedback)
]
