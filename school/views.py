from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from .forms import StudentForm, BookForm, SchoolForm
from .models import (
    Student, School, Book
)


@login_required()
def search_id(request):
    id = request.GET.get('id')
    payload = []
    if id:
        students = Student.objects.filter(id__icontains=id)

        for objs in students:
            payload.append(objs.id)
    payload = list(set(payload))
    return JsonResponse({'status': 200, 'data': payload})


@login_required()
def search_name(request):
    name = request.GET.get('name')
    payload = []
    if name:
        students = Student.objects.filter(first_name__icontains=name)

        for objs in students:
            payload.append(objs.first_name + ' ' + objs.last_name)
    payload = list(set(payload))
    return JsonResponse({'status': 200, 'data': payload})



@method_decorator(login_required(redirect_field_name=''), name='dispatch')
class StudentHomeView(View):
    def get(self, request, *args, **kwargs):
        student = None
        context = {}
        id = self.request.GET.get('student-id', None)
        name = self.request.GET.get('student-name', None)
        if id:
            student = Student.objects.filter(id=id).select_related('school').prefetch_related(
                'bookshistorywithstudent_set').first()
            context['student'] = student
            context['student_id'] = id
        elif name:
            breakpoint()
            student = Student.objects.filter(first_name=name.split(' ')[0],
                     last_name=name.split(' ')[1]).prefetch_related('school', 'bookshistorywithstudent_set').first()

            context['student'] = student
            context['student_name'] = name

        print(id, name)
        return render(self.request, template_name='Home.html', context=context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class StudentView(DetailView):
    model = Student
    template_name = 'school/student.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class StudentCreateView(CreateView):
    template_name = 'school/student-create.html'
    model = Student
    form_class = StudentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('student', kwargs={'pk': self.object.id})


@method_decorator(login_required(login_url='login'), name='dispatch')
class SchoolView(DetailView):
    model = School
    template_name = 'school/school.html'
    context_object_name = 'school'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class SchoolCreateView(CreateView):
    template_name = 'school/school-create.html'
    model = School
    form_class = SchoolForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('school', kwargs={'pk': self.object.id})


@method_decorator(login_required(login_url='login'), name='dispatch')
class BookView(DetailView):
    model = Book
    template_name = 'school/book.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class BookCreateView(CreateView):
    template_name = 'school/book-create.html'
    model = Book
    form_class = BookForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('book', kwargs={'pk': self.object.id})
