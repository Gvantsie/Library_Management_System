from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'password', 'full_name', 'personal_number', 'birth_date')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',
                       'full_name',
                       'personal_number',
                       'birth_date',
                       'password1',
                       'password2',
                       'is_staff',
                       'is_superuser'),
        }),
    )
    list_display = ['email', 'full_name', 'personal_number', 'birth_date', 'is_staff', 'is_superuser']
    search_fields = ('email', 'full_name', 'personal_number')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
