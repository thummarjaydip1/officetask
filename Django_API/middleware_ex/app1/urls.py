from django.urls import path
from app1 import views

urlpatterns = [
    path("",views.my_view),
    path("test/",views.test_view),
    path("template/",views.template_view),
    path("exception/",views.exception_view),
]

