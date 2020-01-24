from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from rooms.models import Room

# Register your models here.


class RoomInline(admin.StackedInline):

    model = Room


@admin.register(models.User)  # Decorator
class CustomUserAdmin(UserAdmin):

    """User Custom Model Definition"""

    inlines = (RoomInline,)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthday",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )

    # 기본적으로 UserAdmin을 상속받아 쓰고 있으므로 기존의 filter에 추가하여 설정해야함
    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
    )


# decorator를 쓰지 않고 admin 등록하는 방법
# admin.site.register(models.User, CustomUserAdmin)
