from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Student

class StudentCreate(CreateView):
    model = Student
    fields = ["name", "age", "city"]
    template_name = "student_form.html"
    success_url = reverse_lazy('display')

class StudentList(ListView):
    model = Student
    template_name = "index.html"
    context_object_name = "data"

class StudentUpdate(UpdateView):
    model = Student
    fields = ["name","age","city"]
    template_name = "student_form.html"
    success_url = reverse_lazy("display")

class StudentDelete(DeleteView):
    model = Student
    template_name = "delete_student.html"
    success_url = reverse_lazy("display")