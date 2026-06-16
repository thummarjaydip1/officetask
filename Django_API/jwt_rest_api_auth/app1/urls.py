from django.urls import path
from app1 import views
from  rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from app1.views import *

urlpatterns = [
    path('auth/register/',RegisterView.as_view(),name="auth_register"),
    path('auth/login/',LoginView.as_view(),name="auth_login"),
    path('token/',TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('token/refresh/',TokenRefreshView.as_view(),name="token_refresh"),
    path('dashboard/',DashboardView.as_view(),name="dashboard"),
]
