from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'personal_number', 'birth_date', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('personal_number', 'birth_date')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
