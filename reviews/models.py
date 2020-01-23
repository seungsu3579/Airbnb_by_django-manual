from django.db import models
from core import models as core_models

# Create your models here.


class Review(core_models.TimeStampedModel):

    """Review Model Definition"""

    review = models.TextField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    cleaniness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room.name} - {self.review}"

    def rating_average(self):
        avg = (
            self.accuracy
            + self.communication
            + self.cleaniness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)

    # short_description으로 admin에 보여질 이름을 설정할 수 있음
    rating_average.short_description = "AVG."
