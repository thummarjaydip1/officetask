from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer
import datetime


@api_view(["POST"])
def add_student(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message" : "Student Data Added Successfully",
            "data" : serializer.data
        })
    return Response(serializer.errors)


@api_view(["GET"])
def get_all_student(request):
    student = Student.objects.all()
    serializer = StudentSerializer(student, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_by_id_student(request, id):
    try:
        student = Student.objects.get(id=id)
    except:
        return Response({"message" : "Student does not Exists"})
    serializer = StudentSerializer(student)
    return Response(serializer.data)


@api_view(["PATCH"])
def update_one_field_student(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response({"message" : "Student Does Not Exists"})
    
    serializer = StudentSerializer(student, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message" : "student record update successfully",
            "updated record" : serializer.data
        })
    return Response(serializer.errors)


@api_view(["PUT"])
def update_full_record_student(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response({"message" : "Student Does Not Exists"})

    serializer = StudentSerializer(student, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message" : "student record update successfully",
            "updated record" : serializer.data
        })
    return Response(serializer.errors)


@api_view(["DELETE"])
def delete_student_record(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response({"message": "Student Does Not Exists"})

    student.delete()
    return Response({
        "message" : "Student record deleted successfully"
    })


@api_view(["GET"])
def get_student_search(request):
    name = request.GET.get("name")
    student = Student.objects.all()

    if name:
        student = Student.objects.filter(name__icontains=name)

    serializer = StudentSerializer(student, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_student_filter(request):
    name = request.GET.get("name")
    email = request.GET.get("email")
    address = request.GET.get("address")

    student = Student.objects.all()

    if name:
        student = Student.objects.filter(name=name)

    if email:
        student = Student.objects.filter(email=email)

    if address:
        student = Student.objects.filter(address=address)

    serializer = StudentSerializer(student, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_student_age(request, id):
    student = Student.objects.get(id=id)

    birth_date = student.birth_date
    today = datetime.datetime.today().date()

    age_year = today.year - birth_date.year

    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age_year -= 1

    age_day = (today - birth_date).days
    print(today - birth_date)

    age_month = age_year * 12 + (today.month - birth_date.month)

    if today.day < birth_date.day:
        age_month -= 1

    return Response({
        "birth_date" : birth_date,
        "today_date" : today,
        "age_year" : age_year,
        "age_month" : age_month,
        "age_day" : age_day
    })