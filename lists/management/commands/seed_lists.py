import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from django.contrib.admin.utils import flatten
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):

    help = "Create Fake Lists"

    def add_arguments(self, parser):

        parser.add_argument(
            "--number", default=1, type=int, help="How many users do you want create?"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(
            list_models.List, number, {"user": lambda x: random.choice(users)},
        )
        created_list = seeder.execute()

        # Image Fake 할당
        # 생성된 Data의 pk list를 리턴 함
        created_clean = flatten(list(created_list.values()))
        for pk in created_clean:
            list_model = list_models.List.objects.get(pk=pk)
            for k in random.choices(list(rooms), k=random.randint(3, 20)):
                list_model.rooms.add(k)
        self.stdout.write(self.style.SUCCESS(f"{number} Lists Created!"))
