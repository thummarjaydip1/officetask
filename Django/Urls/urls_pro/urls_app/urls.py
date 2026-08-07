from django.urls import path
from urls_app import views
from django.urls import re_path
from .views import ProductListView

urlpatterns = [
    # path('books/', views.book_index, name='book_index'),
    # path('books/<int:pk>/', views.book_detail, name='book_detail'),
    # path('books/genre/<str:genre>/', views.books_by_genre, name='books_by_genre'),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    # re_path(r'^blog/(?P<blog_id>\d+)/$', views.blog_detail, name='blog_detail'),

    path("product/", ProductListView.as_view(), name="product"),
]