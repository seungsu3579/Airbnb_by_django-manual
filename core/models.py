from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):

    """Time Stamped Model"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # DateTimeField에는 auto_add 기능이 있다.
    # auto_now=True : save할때 기록
    # auto_now_add=True : model을 생성할때 기록

    # 추상클래스 설정 >> database에 저장되지 않음
    class Meta:
        abstract = True
