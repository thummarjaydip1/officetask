from django.urls import path
from .views import *
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [

    path("add-student/", StudentCreateView.as_view()),

    path("pagination-student/", StudentPaginationView.as_view()),

    path("filter-student/", StudentFilterView.as_view()),

    path("search-student/", StudentSearchView.as_view()),

    path("ordering-student/", StudentOrderingView.as_view()),

    path("exception/", ExceptionGenerate.as_view()),

    path("caching-student/", cache_student_list),

    path("caching-clear/", clear_cache),



    # <----------------------- OPEN API ----------------------->
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger',),
    path('swagger/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
