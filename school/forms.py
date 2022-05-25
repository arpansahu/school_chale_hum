from django.forms import TextInput, EmailInput, TypedChoiceField, NullBooleanSelect, ModelChoiceField, Select, \
    ModelMultipleChoiceField, CheckboxSelectMultiple
from django.urls import reverse

from school.models import Student, Book, School, BooksHistoryWithStudent
from django import forms


class StudentForm(forms.ModelForm):
    book = ModelMultipleChoiceField(queryset=Book.objects.all(), widget=CheckboxSelectMultiple(attrs={}),
                                    required=False,
                                    help_text="Select the Book (if any)"
                                    )

    school = ModelChoiceField(queryset=School.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
                              required=False,
                              help_text="Select the School (if any)"
                              )

    class Meta:
        model = Student
        fields = (
            'first_name',
            'last_name',
            'email',
            'gender',
            'school',
            'book'
        )

        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'gender': Select(attrs={'class': 'form-control'}, ),
        }

    def save(self, commit=True, *args, **kwargs):
        student = super(StudentForm, self).save(commit=True)

        for book_obj in self.cleaned_data['book']:
            history = BooksHistoryWithStudent(
                book_id=book_obj.id,
                student=student
            )
            history.save()

        return super().save()


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = (
            'name',
            'country_code',
            'phone_number',
        )

        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'country_code': TextInput(attrs={'class': 'form-control'}),
            'phone_number': TextInput(attrs={'class': 'form-control'}),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            'name',
            'pages',
        )

        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'pages': TextInput(attrs={'class': 'form-control'}),
        }
