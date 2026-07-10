from django.shortcuts import render
from rest_framework import viewsets

from .serializers import *
from .models import *

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["POST"])
def add_category(request):
    serializer = CategorySerializer(data = request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message" : "Category Add Successfully",
            "added_data" : serializer.data
        })
    return Response(serializer.errors)


@api_view(["GET"])
def get_category(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data)

@api_view(["PUT"])
def update_category(request, id):
    try:
        category = Category.objects.get(id = id)
    except Category.DoesNotExist:
        return Response({"message" : "Category does not Exists"})

    serializer = CategorySerializer(category, data = request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message" : "Category Updated Successfully",
            "updated_data" : serializer.data
        })
    return Response(serializer.errors)


@api_view(["DELETE"])
def delete_category(request, id):
    try:
        category = Category.objects.get(id = id)
    except Category.DoesNotExist:
        return Response({"message" : "Category does not Exists"})

    category.delete()

    return Response({"message" : "Category Deleted Successfully"})



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@api_view(["GET"])
def search_product(request):
    
    data = Product.objects.all()
    name = request.GET.get("name")

    if name:
        data = data.filter(name__icontains=name)

    serializer = ProductSerializer(data, many=True)
    return Response(serializer.data)


# @api_view(["GET"])
# def filter_product(request):
#     products = Product.objects.all()

#     category_name = request.GET.get("category")

#     if category_name:
#         category = Category.objects.filter(name=category_name).first()

#         if category:
#             products = products.filter(category=category)

#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)
