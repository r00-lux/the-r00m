from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users import models


class UserAdmin(BaseUserAdmin):
    """Admin page for users."""
    # How to order objects on the admin page.
    ordering = ['id']

    # Columns to display.
    list_display = ['username', 'email', 'name']

    # Fields to display on an individual object page.
    fieldsets = ((None, {
        'fields': ('email', 'password')
    }), ('Permissions', {
        'fields': ('is_active', 'is_staff', 'is_superuser')
    }), ('Dates', {
        'fields': ('last_login', )
    }))

    # Read-only fields.
    readonly_fields = ['last_login']

    # Fields to show on admin create user page.
    add_fieldsets = ((None, {
        'fields': ('email', 'password1', 'password2', 'name', 'is_active',
                   'is_staff', 'is_superuser')
    }), )


admin.site.register(models.User, UserAdmin)
