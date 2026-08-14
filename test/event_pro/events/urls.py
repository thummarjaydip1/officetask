from django.urls import path
from events import views

urlpatterns = [
    path("", views.index, name="index"),

    path("add_event/", views.add_event, name="add_event"),
    path("list_event/", views.list_event, name="list_event"),
    path("detail_event/<int:id>/", views.detail_event, name="detail_event"),
    path("update_event/<int:id>/", views.update_event, name="update_event"),
    path("delete_event/<int:id>/", views.delete_event, name="delete_event"),

    path("add_attendee/", views.add_attendee, name="add_attendee"),
    path("list_attendee/", views.list_attendee, name="list_attendee"),
    path("update_attendee/<int:id>/", views.update_attendee, name="update_attendee"),
    path("delete_attendee/<int:id>/", views.delete_attendee, name="delete_attendee"),

    path("add_session/", views.add_session, name="add_session"),
    path("list_session/", views.list_session, name="list_session"),
    path("update_session/<int:id>/", views.update_session, name="update_session"),
    path("delete_session/<int:id>/", views.delete_session, name="delete_session"),
]
