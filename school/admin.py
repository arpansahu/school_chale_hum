from django.contrib import admin
from school.models import Student, School, Book, BooksHistoryWithStudent

admin.site.register(Student)
admin.site.register(School)
admin.site.register(Book)
admin.site.register(BooksHistoryWithStudent)
