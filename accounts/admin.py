from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from . models import Account, Profile

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ['username','email', 'is_active', 'is_admin']
    readonly_fields = ['last_login', 'date_joined', 'email', 'username', 'password']

        # Add fieldsets to customize the user details form in the admin
    fieldsets = (
        ('Personal Info', {'fields': ('email', 'username','password')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_staff', 'is_superuser','user_permissions', 'groups')}),
        ('Important dates', {'fields': ('date_joined', 'last_login')}),
    )

    # Customize the filter_horizontal for 'user_permissions' and 'groups'
    filter_horizontal = ('user_permissions', 'groups')


admin.site.register(Account, AccountAdmin)
admin.site.register(Profile)

