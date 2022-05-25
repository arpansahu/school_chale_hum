from django.core.management.base import BaseCommand
from school.models import (
    School,
    Book,
    Student,
    BooksHistoryWithStudent
)

import pandas as pd
from random import randint


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def startup():
    df = pd.read_excel(io='dummy_data.xls')
    for index, row in df.iterrows():
        # breakpoint()
        row_first_name = row['first_name']
        row_last_name = row['last_name']
        row_email = row['email']
        row_gender = row['gender']
        row_school = row['school']
        row_book = row['books']

        print(row_first_name, row_last_name, row_email, row_gender, row_school, row_book)

        if str(row_school) != 'nan':
            school = School.objects.filter(name=row_school).first()
            if not school:
                school = School(
                    name=row_school,
                    country_code='+' + str(randint(0, 150)),
                    phone_number=random_with_N_digits(10)
                )
                school.save()
        else:
            school = None


        if row_gender == 'Male':
            row_gender = 1
        elif row_gender == 'Female':
            row_gender = 2
        else:
            row_gender = 0

        student = Student.objects.filter(first_name=row_first_name, last_name=row_last_name, email=row_email,
                                         gender=row_gender).first()

        if not student:
            student = Student(
                first_name=row_first_name,
                last_name=row_last_name,
                email=row_email,
                gender=row_gender,
                school=school
            )
            student.save()

        if str(row_book) != 'nan':
            book = Book.objects.filter(name=row_book).first()
            if not book:
                book = Book(
                    name=row_book,
                    pages=randint(100, 500)
                )
                book.save()

            book_history = BooksHistoryWithStudent.objects.filter(book=book, student=student).first()
            if not book_history:
                book_history = BooksHistoryWithStudent(
                    book_id=book.id,
                    student_id=student.id,
                    read=randint(100, book.pages)
                )
                book_history.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        startup()
