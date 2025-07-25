from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.admin import ModelAdmin
from unfold.admin import ModelAdmin


class CustomUserAdmin(ModelAdmin):
    list_display = ("email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active",'otp','otp_expiry','otp_max_tries')}),
        ("Important Dates", {"fields": ("RegistrationDate",)}),
        
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email", )
    readonly_fields = ("RegistrationDate",)
    ordering = ("email",)
    namespace = 'users'


admin.site.register(User, CustomUserAdmin)



