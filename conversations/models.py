from django.db import models
from core import models as core_models
from users import models as user_models

# Create your models here.


class Conversation(core_models.TimeStampedModel):
    """ Conversation Definition """

    participants = models.ManyToManyField(user_models.User, blank=True)

    def __str__(self):
        user_names = []
        for user in self.participants.all():
            user_names.append(user.username)

        user_names_string = ", ".join(user_names)
        return f"{user_names_string} : {str(self.created)}"

    def count_messages(self):
        return self.messages.count()

    count_messages.short_description = "Number of Messages"

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "Number of Participants"

    pass


class Message(core_models.TimeStampedModel):

    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    message = models.TextField()

    def __str__(self):
        return f"{self.user} : {self.message}"

    pass
