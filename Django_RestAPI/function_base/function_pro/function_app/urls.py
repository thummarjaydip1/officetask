from django.urls import path
from function_app import views

urlpatterns = [
    path("add-student/", views.add_student),

    path("get-student/", views.get_all_student),

    path("get-student/<int:id>/", views.get_by_id_student),

    path("update-student-field/<int:id>", views.update_one_field_student),

    path("update-student-record/<int:id>", views.update_full_record_student),

    path("delete-student-record/<int:id>", views.delete_student_record),

    path("get-student-search/", views.get_student_search),

    path('get-student-filter/', views.get_student_filter),

    path('get-student-age/<int:id>', views.get_student_age)
]
