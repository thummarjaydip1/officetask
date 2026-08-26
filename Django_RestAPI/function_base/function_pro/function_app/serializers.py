from rest_framework import serializers
from .models import Student

# class StudentSerializer(serializers.ModelSerializer):
#     name = serializers.CharField()
#     age = serializers.IntegerField()
#     email = serializers.EmailField()
#     address = serializers.CharField()
#     pocket_money = serializers.BigIntegerField()
#     image = serializers.ImageField()
#     birth_date = serializers.DateField()


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = "__all__"
