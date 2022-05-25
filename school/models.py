from django.db import models
from django.utils.translation import gettext_lazy as _
from school_chale_hum.models import AbstractBaseModel

# Create your models here.

NO_GENDER = 0
MALE = 1
FEMALE = 2


class School(AbstractBaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300, unique=True)
    country_code = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Book(AbstractBaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300, unique=True)
    pages = models.IntegerField(null=False)

    def __str__(self):
        return self.name


class Student(AbstractBaseModel):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300, null=True, default=None)
    email = models.EmailField(max_length=50, null=False, unique=True)

    GENDER_CHOICES = (
        (NO_GENDER, _("")),
        (MALE, _("Male")),
        (FEMALE, _("Female")),
    )
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICES,
        default=NO_GENDER,
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class BooksHistoryWithStudent(AbstractBaseModel):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    read = models.IntegerField(auto_created=True, default=0)

    class Meta:
        unique_together = ('book', 'student',)
