from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from junior_hunter.forms import (
    RegistrationCompanyDefaultUserForm,
    RegistrationCompanyForm
)

from junior_hunter.models import Specialty, Company, Vacancy, DefaultUser, CompanyUser


class MainView(View):
    def get(self, request):
        specialties = Specialty.objects.all()
        companies = Company.objects.all()
        context = {
            'specialties': specialties,
            'companies': companies
        }
        return render(request, 'index.html', context=context)


class VacanciesView(View):
    def get(self, request):
        vacancies = Vacancy.objects.all()
        context = {
            'vacancies': vacancies
        }
        return render(request, 'vacancies.html', context=context)


class VacancyIdView(View):
    def get(self, request, vacancy_id):
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        if not vacancy:
            return HttpResponseNotFound(f'Нет вакансии с id {vacancy_id}.'
                                        f' Перейти на <a href="/">Главную страницу</a>')
        companies_in_vacancy = vacancy.company
        context = {
            'vacancy': vacancy,
            'companies_in_vacancy': companies_in_vacancy
        }
        return render(request, 'vacancy.html', context=context)


class CompanyIdView(View):
    def get(self, request, company_id):
        company = Company.objects.filter(id=company_id).first()
        if not company:
            return HttpResponseNotFound(f'Нет компании с id {company_id}.'
                                        f' Перейти на <a href="/">Главную страницу</a>')
        company_vacancies = Vacancy.objects.filter(company_id=company)
        context = {
            'company': company,
            'company_vacancies': company_vacancies
        }
        return render(request, 'company.html', context=context)


class VacancyInCategoryView(View):
    def get(self, request, vacancy_in_category):
        specialty = Specialty.objects.filter(code=vacancy_in_category).first()
        if not specialty:
            return HttpResponseNotFound(f'Нет категории {vacancy_in_category}.'
                                        f' Перейти на <a href="/">Главную страницу</a>')
        vacancy_in_category = Vacancy.objects.filter(speciality_id=specialty)
        context = {
            'specialty': specialty,
            'vacancies_in_category': vacancy_in_category,
        }
        return render(request, 'vacancies_search.html', context=context)


def registration_company_view(request):
    """Регистрация компанни. Передается две формы для заполнения двух моделей
   DefaultUser и CompanyUser"""

    form_default_user = RegistrationCompanyDefaultUserForm()
    form_company = RegistrationCompanyForm()
    context = {}
    if request.user.is_authenticated:
        return redirect('vacancies')
    if request.POST:
        form_default_user = RegistrationCompanyDefaultUserForm(request.POST)
        form_company = RegistrationCompanyForm(request.POST)
        if form_default_user.is_valid() and form_company.is_valid():
            email = form_default_user.cleaned_data['email']
            raw_pass = form_default_user.cleaned_data.get('password1')
            first_name = form_company.cleaned_data['first_name']
            last_name = form_company.cleaned_data['last_name']
            user = DefaultUser.objects.create_user(email=email, password=raw_pass)
            company_user = CompanyUser(first_name=first_name, last_name=last_name, user=user)
            company_user.save()
            # user_auth = authenticate(
            #     email=email,
            #     password=raw_pass,
            # )
            login(request, user)
            return redirect('vacancies')
    context = {
        'form_default_user': form_default_user,
        'form_company': form_company
    }
    return render(request, 'register_company.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('index')


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ошибка 404! Попробуйте открыть другую страницу')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка 500! Попробуйте открыть другую страницу')
