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
                    "Bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )

    # <- column들을 각 성격대로 모아줌

    pass
