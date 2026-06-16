from django.urls import path
from app1 import views

urlpatterns = [
    path('login/',views.login_user,name="login"),
    path('register/',views.register_user,name="register"),
    path('logout/',views.logout_user,name="logout"),
    path('home/',views.home,name="home"),
]
