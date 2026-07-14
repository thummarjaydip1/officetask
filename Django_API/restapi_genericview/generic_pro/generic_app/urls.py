from django.urls import path
from generic_app import views
from .views import CreateContactView, DisplayContactView, RetrieveContactView, UpdateContactView, DeleteContactView, SearchContactView, FeedbackListView, FeedbackDetailView

urlpatterns = [
    # CONTACT API
    path("add-contact/", CreateContactView.as_view()),
    path("get-contact/", DisplayContactView.as_view()),
    path("detail-contact/<int:pk>/", RetrieveContactView.as_view()),
    path("update-contact/<int:pk>", UpdateContactView.as_view()),
    path("delete-contact/<int:pk>/", DeleteContactView.as_view()),
    path("search-contact/", SearchContactView.as_view()),

    # FEEDBACK API
    path("feedback-list/", FeedbackListView.as_view()),
    path("feedback-detail/<int:pk>/", FeedbackDetailView.as_view())
]
