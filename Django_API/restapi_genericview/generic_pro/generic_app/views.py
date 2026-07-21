from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework import filters
from rest_framework import generics

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Contact, Feedback
from .serializers import ContactSerializer, FeedbackSerializer


from rest_framework.decorators import api_view
# http://127.0.0.1:8000/add-contact/
class CreateContactView(CreateModelMixin, GenericAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

# http://127.0.0.1:8000/get-contact/
class DisplayContactView(ListModelMixin, GenericAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    

# http://127.0.0.1:8000/detail-contact/3/
class RetrieveContactView(RetrieveModelMixin, GenericAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    

# http://127.0.0.1:8000/update-contact/2
class UpdateContactView(UpdateModelMixin, GenericAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    

# http://127.0.0.1:8000/delete-contact/4/
class DeleteContactView(DestroyModelMixin, GenericAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    



# http://127.0.0.1:8000/feedback-list/
class FeedbackListView(APIView):
    def get(self, request):
        feedback = Feedback.objects.all()
        serializer = FeedbackSerializer(feedback, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request):
        serializer = FeedbackSerializer(data = request.data)
        
        if serializer.is_valid(): 
            serializer.save()
            return Response({
                "message" : "Feedback send successfuly",
                "sended_feedback" : serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors)
    

# http://127.0.0.1:8000/feedback-detail/4/
class FeedbackDetailView(APIView):
    def get(self, request, pk):
        try:
            feedback = Feedback.objects.get(pk = pk)
        
        except Feedback.DoesNotExist:
            return Response({"message" : "Feedback not found"})

        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def put(self, request, pk):
        try:
            feedback = Feedback.objects.get(pk = pk)
        
        except Feedback.DoesNotExist:
            return Response({"message" : "Feedback not found"})
            
        serializer = FeedbackSerializer(feedback, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message" : "Feedback updated successfully",
                "updated_feedback" : serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors)
    

    def delete(self, request, pk):
        try:
            feedback = Feedback.objects.get(pk = pk)
        
        except Feedback.DoesNotExist:
            return Response({"message" : "Feddback not found"})
        
        feedback.delete()

        return Response({
            "message" : "Feedback delete successfully"
        }, status=status.HTTP_200_OK)
