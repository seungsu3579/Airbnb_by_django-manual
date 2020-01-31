from django.core.management.base import BaseCommand
from rooms.models import Amenity


class Command(BaseCommand):

    help = "Create Fake Amenities Data"

    def handle(self, *args, **options):

        amenities = [
            "Kitchen",
            "Shampoo",
            "Heating",
            "Air conditioning",
            "Wifi",
            "Hangers",
            "Iron",
            "Hair dryer",
            "Laptop friendly workspace",
            "TV",
            "Private bathroom",
            "Washer",
            "Dryer",
            "Breakfast",
            "Indoor fireplace",
            "Crib",
            "High chair",
            "Self check_in",
            "Free parking on premises",
            "Gym",
            "Hot tub",
            "Pool",
            "Smoke detector",
            "Carbon monoxide detector",
        ]

        for a in amenities:
            Amenity.objects.create(name=a)

        self.stdout.write(self.style.SUCCESS("Amenities Created"))
