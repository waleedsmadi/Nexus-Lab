from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AuthUser


class AuthUserAdmin(UserAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active']
    list_display_links = ['username']
    list_filter = ['is_active', 'is_staff']
    ordering = ['-date_joined']
    search_fields = ['username', 'email']

    fieldsets = UserAdmin.fieldsets + (
        ("Image", {"fields": ('img',)}),
    )


    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Email', {'fields': ('email',)}),
        ('Image', {'fields': ('img',)}),
    )

admin.site.register(AuthUser, AuthUserAdmin)