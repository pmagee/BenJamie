from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display=['email', 'username', 'name']
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("name",)}),)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "name"),
            },
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)