from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User admin """

    fieldsets = UserAdmin.fieldsets
    fieldsets = fieldsets + (
        (
            "Custom profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                ),
            },
        ),
    )

    # raw id로 찾을 수 있도록 만들어줌.

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
    )

    # <- column들을 각 성격대로 모아줌

    pass
