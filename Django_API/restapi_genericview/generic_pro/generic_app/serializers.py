from rest_framework import serializers
from .models import Contact, Feedback


class ContactSerializer(serializers.ModelSerializer):

    class Meta:

        model = Contact
        fields = "__all__"
    
class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:

        model = Feedback
        fields = ["id", "name", "email", "message"]
        # read_only_field = ["id"]