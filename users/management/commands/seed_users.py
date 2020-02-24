from django.core.management.base import BaseCommand

from django_seed import Seed

from users import models as users_models


class Command(BaseCommand):

    help = "This command creates amenities"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--times", help="How many times do you want me to tell you that I love you"
    #     )

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, help="how many user do you want to create?"
        )

    def handle(self, *args, **kargs):
        number = int(kargs.get("number"))  # key , default value
        seeder = Seed.seeder()
        seeder.add_entity(
            users_models.User, number, {"is_staff": False, "is_superuser": False}
        )
        seeder.execute()
