from django.db import models
from django_countries.fields import CountryField
from core import models as core_models
from users import models as user_models

# Create your models here.


class AbstractItem(core_models.TimeStampedModel):

    """Abstract Item"""

    name = models.CharField(max_length=80)

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
    file = models.ImageField()
    room = models.ForeignKey("Room", on_delete=models.CASCADE)

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

    # 이때 foreign key와 manytomany에서는 string으로 model을 표현하면 model에 접근 가능
    # 물론 string으로 안해도 되지만 그러면 model 생성 순서에 영향을 받아 error가 뜨기도 함
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room_type = models.ForeignKey("RoomType", on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField("Amenity", blank=True)
    facilities = models.ManyToManyField("Facility", blank=True)
    house_rules = models.ManyToManyField("HouseRule", blank=True)

    def __str__(self):
        return self.name
