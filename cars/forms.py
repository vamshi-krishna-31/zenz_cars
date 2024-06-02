from django import forms
from django.contrib.auth.models import User
from .models import EmployeeProfile


class UserRegistrationForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    mobile_number = forms.CharField(max_length=15)
    location = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    first_name = forms.CharField(label='Name', max_length=30)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            EmployeeProfile.objects.create(
                user=user,
                mobile_number=self.cleaned_data['mobile_number'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                location=self.cleaned_data['location']
            )
        return user


class UploadFileForm(forms.Form):
    file = forms.FileField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)