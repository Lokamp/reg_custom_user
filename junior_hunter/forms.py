from django import forms
from django.contrib.auth.forms import UserCreationForm

from junior_hunter.models import DefaultUser, CompanyUser


class RegistrationCompanyDefaultUserForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = DefaultUser
        fields = ('email',)


class RegistrationCompanyForm(forms.ModelForm):

    class Meta:
        model = CompanyUser
        fields = ('first_name', 'last_name')




