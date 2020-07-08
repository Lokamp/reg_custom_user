
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
            # form_default_user.save()
            email = form_default_user.cleaned_data['email']
            raw_pass = form_default_user.cleaned_data['password1']
            # user = DefaultUser.objects.create(
            #     email=email,
            #     password=password
            # )
            # user.save()
            user = DefaultUser(
                email=email,
                password=raw_pass
            )
            user.save()
            first_name = form_company.cleaned_data['first_name']
            last_name = form_company.cleaned_data['last_name']
            user_company = CompanyUser(
                first_name=first_name,
                last_name=last_name,
                user=user
            )
            user_company.save()
            user_auth = authenticate(
                email=email,
                password=raw_pass
            )
            login(request, user_auth)
            return redirect('vacancies')
    context = {
        'form_default_user': form_default_user,
        'form_company': form_company
    }
    return render(request, 'register_company.html', context=context)
