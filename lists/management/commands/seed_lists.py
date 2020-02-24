import random

from django.core.management.base import BaseCommand
from django_seed import Seed
from django.contrib.admin.utils import flatten
from reviews import models as review_models
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models

NAME = "lists"


class Command(BaseCommand):

    help = f"This command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            type=int,
            default=1,
            help=f"How many numbers do you want to create {NAME}",
        )

    def handle(self, *args, **kargs):
        number = int(kargs.get("number"))  # key , default value
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        seeder = Seed.seeder()
        seeder.add_entity(
            list_models.List, number, {"user": lambda x: random.choice(users),},
        )

        created_lists = seeder.execute()
        created_clean = flatten(list(created_lists.values()))

        for pk in created_clean:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            list_model.room.add(*to_add)

        self.stdout.write(
            self.style.SUCCESS(f"{len(created_clean)}_{NAME} object created")
        )
