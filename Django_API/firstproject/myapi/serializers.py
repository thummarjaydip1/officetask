from rest_framework import serializers
from myapi.models import *

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        # field = ['name','age','email']

class EmployeeSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name',read_only=True)
    class Meta:
        model = Employee
        fields = '__all__'

# contact
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"