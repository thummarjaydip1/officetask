from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Feedback

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ["id","username","password","email"]
        read_only_field = ["id"]
        

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", "")
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = Feedback
        fields = "__all__" 