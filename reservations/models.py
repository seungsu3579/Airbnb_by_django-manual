from django.db import models
from core import models as core_models

# 장고에서 타임을 불러올 때 쓰는 모델
from django.utils import timezone

# Create your models here.


class Reservation(core_models.TimeStampedModel):

    """Reservation Model Definition"""

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "pending"),
        (STATUS_CONFIRMED, "confirmed"),
        (STATUS_CANCELED, "canceled"),
    )

    status = models.CharField(
        choices=STATUS_CHOICES, max_length=10, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room.name} - {self.guest.username}"

    def in_progress(self):
        today = timezone.now().date()
        return today >= self.check_in and today <= self.check_out

    def is_finished(self):
        today = timezone.now().date()
        return today > self.check_out

    def before_in(self):
        today = timezone.now().date()
        return today < self.check_in

    # admin page에서 표현될 때 이미지로 표현
    in_progress.boolean = True
    is_finished.boolean = True
    before_in.boolean = True
