from django.urls import path
from blog import views

urlpatterns = [

    path('', views.index, name="index"),
    path('post_detail/<int:id>', views.post_detail, name="post_detail"),

    path('add_tag/', views.add_tag, name="add_tag"),
    path('update_tag/<int:id>', views.update_tag, name="update_tag"),
    path('delete_tag/<int:id>', views.delete_tag, name="delete_tag"),


    path('add_post/', views.add_post, name="add_post"),
    path('update_post/<int:id>', views.update_post, name="update_post"),
    path('delete_post/<int:id>', views.delete_post, name="delete_post"),


    path('add_comment/', views.add_comment, name="add_comment"),
    path('update_comment/<int:id>', views.update_comment, name="update_comment"),
    path('delete_comment/<int:id>', views.delete_comment, name="delete_comment"),

]
