from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """ Conversation admin definition """

    list_display = (
        "__str__",
        "count_messages",
        "count_participants",
    )

    pass


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):

    """ Message admin definition """

    list_display = ("__str__", "created")

    pass
