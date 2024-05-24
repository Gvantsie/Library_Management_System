from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    personal_number = forms.CharField(max_length=20)
    birth_date = forms.DateField()
    is_staff = forms.BooleanField(required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('personal_number', 'birth_date', 'is_staff')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.personal_number = self.cleaned_data["personal_number"]
        user.birth_date = self.cleaned_data["birth_date"]
        user.is_staff = self.cleaned_data.get("is_staff", False)
        if commit:
            user.save()
        return user
