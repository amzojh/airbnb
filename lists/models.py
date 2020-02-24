from django.db import models
from core import models as core_models
from users import models as user_models
from rooms import models as room_models

# Create your models here.


class List(core_models.TimeStampedModel):
    name = models.CharField(max_length=80)
    user = models.ForeignKey(
        user_models.User, related_name="list", on_delete=models.CASCADE
    )
    room = models.ManyToManyField(room_models.Room, blank=True)

    def __str__(self):
        return f"{self.name}"

    def count_rooms(self):
        return self.room.count()

    count_rooms.short_description = "Number of Rooms"

    pass
