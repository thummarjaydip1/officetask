from django.urls import path,include
from rest_framework import routers
from .views import *
from myapi import views # myapi app name

router = routers.DefaultRouter()
router.register(r"companies",CompanyViewSet)
router.register(r"employee",EmployeeViewSet)    
router.register(r"contact",ContactViewSet)

urlpatterns = [
    # path('home/',views.home)
    path('',include(router.urls)),
    path('index/',views.contact_form_add_data,name="index"),
    path('display/',views.contact_form_display_data,name="display"),
    path('update/<int:id>/',views.contact_form_update_data,name="update"),
    path('delete/<int:id>/',views.contact_form_delete_data,name="delete")
]