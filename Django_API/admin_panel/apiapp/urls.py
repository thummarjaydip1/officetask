from django.urls import path, include
from .views import *
from apiapp import views
from rest_framework import routers

# Contact table with API
router = routers.DefaultRouter()
router.register(r"contact-api", ContactViewSet)

urlpatterns = [
    # contact api url
    path("api/", include(router.urls)),
    # contact url
    path("contact_add/", views.contact_add_data, name="contact_add"),
    path("contact_update/<int:id>/", views.contact_update_data, name="contact_update"),
    path("contact_delete/<int:id>/", views.contact_delete_data, name="contact_delete"),
    path("display_data/", views.display_data, name="display_data"),
    # feedback api url
    path("api/feedback-add/", feedback_add),
    path("api/feedback-display/", feedback_display),
    path("api/feedback-display-id/<int:id>/", feedback_display_id),
    path("api/feedback-update/<int:id>/", feedback_update),
    path("api/feedback-delete/<int:id>/", feedback_delete),
    # feedback url
    path("feedback_add/", views.feedback_add_data, name="feedback_add"),
    path(
        "feedback_update/<int:id>/", views.feedback_update_data, name="feedback_update"
    ),
    path(
        "feedback_delete/<int:id>/", views.feedback_delete_data, name="feedback_delete"
    ),
]
