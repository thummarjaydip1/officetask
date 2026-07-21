from django.urls import path
from token_app import views
from .views import *

urlpatterns = [
    path("register/",views.register_user),
    path("get-user/",views.get_user),
    path("update-user/<int:id>/",views.update_user),
    path("delete-user/<int:id>/",views.delete_user),
    path("login/", LoginAPIView.as_view()),
    path("profile/", UserProfile.as_view()),

    path("feedback-list/", FeedbackListView.as_view()),
    path("feedback-detail/<int:pk>/", FeedbackDetailView.as_view()),
]
