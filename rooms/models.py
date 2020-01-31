from django.db import models
from django_countries.fields import CountryField
from core import models as core_models

# Create your models here.


class AbstractItem(core_models.TimeStampedModel):

    """Abstract Item"""

    name = models.CharField(max_length=80)

    # 데이터를 출력할 것을 설정
    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Amenity(AbstractItem):

    """Amenity Object Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class HouseRule(AbstractItem):

    """HouseRule Object Definition"""

    class Meta:
        verbose_name_plural = "House Rules"


class Facility(AbstractItem):

    """Facility Object Definition"""

    class Meta:
        # 데이터가 보여지는 순서도 또한 적용할수 있음
        ordering = ["created"]

        # 장고는 admin에서 자동으로 복수형으로 고쳐보여주는데 이때 복수형을 우리가 설정할 수 있음
        verbose_name_plural = "Facilities"


class RoomType(AbstractItem):

    """RoomType Object Definition"""

    class Meta:
        verbose_name_plural = "Room Types"


class Photo(core_models.TimeStampedModel):

    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    # ImageField 속성값으로 upload_to를 이용하여 MEDIA_ROOT안의 어떤 파일에 저장할건지 설정 가능
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """Room Model"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)

    # 1. 이때 foreign key와 manytomany에서는 string으로 model을 표현하면 model에 접근 가능
    #    물론 string으로 안해도 되지만 그러면 model 생성 순서에 영향을 받아 error가 뜨기도 함
    # 2. related_name = 을 통해 1:n relation 에서 1에서 접근할 때의 naming을 설정할 수 있음 (default는 ~~_set)
    # 3. n:m relation인 ManyToMany에서는 변수명으로 접근 가능 (아래 같은 경우 roomobject.amenities)
    #    ManyToMany에서도 related_name을 통해 반대로 접근할 변수를 설정 가능 (아래 같은 경우 amenityobject.rooms)
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.rating_average()
        if len(all_reviews) != 0:
            return round(all_ratings / len(all_reviews), 2)
        else:
            return 0

    # 어디에서 변경되던 이 모델의 모든 변경은 저장하기 전에 이 메서드를 거쳐 실행됨
    # admin에서의 변경만 intercept하고 싶다면 admin.ModelAdmin의 save_model()를 통해 설정가능
    # admin에서 변경된 경우, save_model이 실행되고 모델의 save가 실행됨
    def save(self, *args, **kwargs):

        self.city = str.capitalize(self.city)
        # super()로 상위 save method를 불러야함
        super(Room, self).save(*args, **kwargs)  # Call the real save() method
