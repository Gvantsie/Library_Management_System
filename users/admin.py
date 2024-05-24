from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'personal_number', 'birth_date', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Personal Info', {'fields': ('personal_number', 'birth_date')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Personal Info', {'fields': ('personal_number', 'birth_date')}),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.is_staff = True  # Ensure that new users added via the admin are staff
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser, CustomUserAdmin)
