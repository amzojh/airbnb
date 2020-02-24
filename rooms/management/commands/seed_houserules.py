from django.core.management.base import BaseCommand
from rooms import models as rooms_models


class Command(BaseCommand):

    help = "This command creates amenities"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--times", help="How many times do you want me to tell you that I love you"
    #     )

    def handle(self, *args, **kargs):
        house_rules = [
            "No Parties or Events.",
            "Only Registered Guests Are Allowed.",
            "No Unregistered Guest.",
            "Clean Your Dirty Dishes Before Check-Out or You Will Charged A Fee.",
            "Do Not Use The Premises For Any illegal Activity.",
            "No Smoking.",
            "Guests Should Dispose Of The Garbage In The Trash Can.",
            "No Shoes Inside The Home Please.",
        ]

        for r in house_rules:
            rooms_models.HouseRule.objects.create(name=r)

        self.stdout.write(self.style.SUCCESS(f"{len(house_rules)} - created"))
