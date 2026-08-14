from django.contrib import admin
from .models import Student, Book

@admin.register(Student)
class StudntAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "age", "addres"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date', 'page', 'available')
    search_fields = ('title', 'author')
    list_filter = ('available', 'publish_date')
    list_editable = ["page"]