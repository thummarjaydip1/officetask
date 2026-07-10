from django.urls import path, include
from restapi_app import views
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register(f"product", ProductViewSet)

urlpatterns = [
    path('products/',include(router.urls)),

    path("add-category/", views.add_category),
    path("get-category/", views.get_category),
    path("update-category/<int:id>/", views.update_category),
    path("delete-category/<int:id>/", views.delete_category),

    path("products/search-product/", views.search_product),
    # path("products/filter-product/", views.filter_product)
]
