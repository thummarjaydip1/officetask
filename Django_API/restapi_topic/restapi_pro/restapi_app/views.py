from django.shortcuts import render
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView

# Pagination and Filtering
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

# Exception
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

# Caching
from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from rest_framework.response import Response

# Searching and Ordering
from rest_framework import filters 

from .serializers import *
from .models import *


# http://127.0.0.1:8000/add-student/
class StudentCreateView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CustomPagination(PageNumberPagination):
    page_size = 2
    page_query_param = "page_num"
#     # page_size_query_param = 'record'        # page_num=2&record=5  five record display
#     # max_page_size = 7                       # max record 7 display 
#     # last_page_strings = "end"               # ?page_num = end      default last change last convert to end
        

# http://127.0.0.1:8000/pagination-student/?page_num=5
class StudentPaginationView(ListModelMixin, GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    

# http://127.0.0.1:8000/filter-student/?name=&age=&email=&address=surat
class StudentFilterView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = "__all__"       # ["name", "age", "email", "address"]


# http://127.0.0.1:8000/search-student/?search=ja
class StudentSearchView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "email"]


# http://127.0.0.1:8000/ordering-student/?ordering=age
class StudentOrderingView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.OrderingFilter]
    # ordering = ["name"]                           # only name ordering


# http://127.0.0.1:8000/exception/
class ExceptionGenerate(APIView):
    def get(self, request):
        age = 40
        if age < 18:
            raise ValidationError(f"You are not aligible for vote -- Age: {age}")
        else:
            raise ValidationError(f"You are not aligible for vote -- Age: {age}")


# http://127.0.0.1:8000/caching-student/
@api_view(["GET"])
@cache_page(30)                             # 30 second caching available
def cache_student_list(request):
    print("this is caching.....")
    student = Student.objects.all()
    serializers = StudentSerializer(student, many=True)
    return Response(serializers.data)


# http://127.0.0.1:8000/caching-clear/
@api_view(["GET"])
def clear_cache(request):
    cache.clear()
    return Response({"msg" : "All cache clear"})
