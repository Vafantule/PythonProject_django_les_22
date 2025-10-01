from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("avatar", "phone", "country")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("avatar", "phone", "country")}),
    )
    list_display = ("email", "username", "phone", "country", "is_active", "is_staff")
    search_fields = ("email", "username", "phone", "country")


admin.site.register(CustomUser, CustomUserAdmin)
