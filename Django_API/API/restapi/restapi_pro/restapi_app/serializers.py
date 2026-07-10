from rest_framework import serializers
from .models import Student, Contact, Feedback

class StudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Student
        fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ["id","name","email","phone","address"]


class FeedbackSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Feedback
        fields = "__all__"