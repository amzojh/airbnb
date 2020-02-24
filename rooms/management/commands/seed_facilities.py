from django.core.management.base import BaseCommand
from rooms import models as rooms_models


class Command(BaseCommand):

    help = "This command creates amenities"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--times", help="How many times do you want me to tell you that I love you"
    #     )

    def handle(self, *args, **kargs):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]

        for f in facilities:
            rooms_models.Facility.objects.create(name=f)

        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} - created"))
