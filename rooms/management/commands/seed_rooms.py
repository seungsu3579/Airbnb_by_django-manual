from django.core.management.base import BaseCommand
from django_seed import Seed

# flatten을 사용하면 중첩된 리스트 등을 하나로 변경시켜준다.
from django.contrib.admin.utils import flatten
import random
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):

    help = "Create Fake Rooms Data"

    def add_arguments(self, parser):
        # type으로 입력받은 값을 string에서 자동으로 변환 가능하다.
        # default 값을 설정해줄수도 있다.
        parser.add_argument(
            "--number", default=1, type=int, help="How many rooms do you want create?"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        house_rules = room_models.HouseRule.objects.all()

        # Seed.seeder()를 통해 Fake Data를 만들수 있다.
        # attribute값으로는 (모델, 개수, 조건(dict))이 있다.
        # seeder가 기본적인 모델은 fake 데이터를 만들지만 Foriegnkey 와  ManyToMany는 구현하지 못함
        # 그렇기에 조건을 추가하여 아래와 같이 표현
        # ImageField 또한 다루기 어려움
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(30, 1000),
                "beds": lambda x: random.randint(1, 10),
                "bedrooms": lambda x: random.randint(1, 10),
                "baths": lambda x: random.randint(1, 10),
                "guests": lambda x: random.randint(1, 15),
            },
        )
        # 실행 시켜줘야 적용이됨
        created_photo = seeder.execute()

        # Image Fake 할당
        # 생성된 Data의 pk list를 리턴 함
        created_clean = flatten(list(created_photo.values()))
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            for k in range(random.randint(5, 15)):
                room_models.Photo.objects.create(
                    room=room,
                    file=f"room_photos/{random.randint(1,31)}.webp",
                    caption=seeder.faker.sentence(),
                )

            # 다대다 관계는 이렇게 추가함
            for a in amenities:
                if random.randint(0, 16) % 3 == 0:
                    room.amenities.add(a)
            for f in facilities:
                if random.randint(0, 16) % 3 == 0:
                    room.facilities.add(f)
            for r in house_rules:
                if random.randint(0, 16) % 3 == 0:
                    room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} Rooms Created!"))
