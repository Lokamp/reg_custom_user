from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from junior_hunter.managers import CustomUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class DefaultUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(
        primary_key=True
    )
    email = models.EmailField(
        verbose_name="Email",
        max_length=60,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    is_employment = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class CompanyUser(DefaultUser):
    user = models.OneToOneField(
        DefaultUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='company'
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=30
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=30
    )
    date_joined = models.DateField(
        verbose_name="Дата регистрации",
        auto_now_add=True
    )
    time_joined = models.TimeField(
        verbose_name="Время регистрации",
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.email} {self.first_name}'


class Specialty(models.Model):
    title = models.CharField(max_length=120)
    code = models.CharField(max_length=20)
    picture = models.CharField(max_length=40)


class Company(models.Model):
    name = models.CharField(max_length=80)
    location = models.CharField(max_length=50)
    logo = models.CharField(max_length=40)
    description = models.CharField(max_length=50)
    employee_count = models.IntegerField()


class Vacancy(models.Model):
    title = models.CharField(max_length=120)
    speciality = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name="vacancies")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    skills = models.CharField(max_length=200)
    description = models.CharField(max_length=150)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()
