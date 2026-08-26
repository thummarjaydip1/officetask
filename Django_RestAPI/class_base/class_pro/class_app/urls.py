from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(f"contact", ContactViewSet)

urlpatterns = [
    path("contacts/", include(router.urls)),

    path("feedback-list/", FeedbackListView.as_view()),
    path("feedback-detail/<int:pk>", FeedbackDetailView.as_view()),

    path("student-list/", StudentListView.as_view()),
    path("student-detail/<int:pk>/", StudentDetailView.as_view()),

    path("employee-add/", EmployeeAddView.as_view()),
    path("employee-list/", EmployeeListView.as_view()),
    path("employee-detail/<int:pk>", EmployeeRetrieveView.as_view()),
    path("employee-update/<int:pk>", EmployeeUpdateView.as_view()),
    path("employee-delete/<int:pk>", EmployeeDeleteView.as_view()),
    path("employee-search/", EmaployeeSearchingView.as_view()),
    path("employee-ordering/", EmployeeOrderingView.as_view()),
    path("employee-pagination/", EmployeePaginationView.as_view()),
    path("employee-caching/", EmployeeCachingView.as_view()),
]