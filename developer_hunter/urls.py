from django.contrib import admin
from django.urls import path, re_path

from junior_hunter.views import (
    MainView,
    VacanciesView,
    VacancyIdView,
    VacancyInCategoryView,
    CompanyIdView,
    registration_company_view,
    logout_view
)
from junior_hunter.views import custom_handler404, custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='index'),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('registration_company/', registration_company_view, name='reg_company'),
    path('logout/', logout_view, name='logout'),
    re_path(r'^vacancies/?(?P<vacancy_id>\d+)?/$', VacancyIdView.as_view(), name='vacancy_id'),
    re_path(r'^companies/?(?P<company_id>\d+)?/$', CompanyIdView.as_view(), name='company_id'),
    re_path(r'^vacancies/cat/?(?P<vacancy_in_category>\w+)?/$', VacancyInCategoryView.as_view(),
            name='vacancy_in_category')
]

handler404 = custom_handler404
handler500 = custom_handler500
