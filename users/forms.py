
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    personal_number = forms.CharField(max_length=20)
    birth_date = forms.DateField()

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('personal_number', 'birth_date', 'is_staff')

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date and birth_date > timezone.now().date():
            raise forms.ValidationError("Birth date cannot be in the future")
        return birth_date

    def save(self, commit=True):
        user = super().save(commit=False)
        user.personal_number = self.cleaned_data["personal_number"]
        user.birth_date = self.cleaned_data["birth_date"]
        user.is_staff = self.cleaned_data.get("is_staff", False)
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'