from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.

# admin안에 admin을 넣기 위함.(주로 ForiegnKey 속성 값을 추가함)
# admin.TabularInlin, admin.StackedInline 2가지 종류가 있음
class PhotoInline(admin.TabularInline):
    # 집어넣을 모델 설정을 해줘야함
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """Room Admin Definition"""

    # admin 안에 admin 을 넣기 위해 위에서 생성한 class 추가
    inlines = (PhotoInline,)

    # 세부 데이터를 보여줄때 group화
    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        ("Space", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        ("Time Info", {"fields": ("check_in", "check_out", "instant_book")}),
        (
            "More About The Space",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        ("Last Details", {"fields": ("host",)}),
    )

    # 전체 데이터 보여줄때 함께 보여줄 column 설정
    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
    )

    # admin 필터 설정   host__superhost 이런식으로 ForiegnKey의 속성값에 접근 가능
    list_filter = (
        "host__superhost",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    # ordering으로 admin에서 보여질 때 정렬할 수 있다.
    ordering = (
        "country",
        "city",
    )

    # 수많은 유저들이 있을때 host를 select하기 어렵기에 간단히 검색가능하게 함
    raw_id_fields = ("host",)

    # admin 검색창 검색 column 설정 (^,=,@)
    search_fields = ("^city", "^host__username")

    # ManyToMany Relation에서 작동하는 속성 >> admin에서 다르게 보여짐
    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    # admin class 내부함수를 통해 ManyToMany도 보여질수 있다.
    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = (
        "name",
        "used_by",
    )

    # admin패널 안에서만 필요한 정보는 admin.py에 함수를 생성하고
    # 전체 데이터에 필요한 정보같은 경우는 models.py에 함수를 생성한다.
    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Photo Admin Definition"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        # django.utils.html 에서 mark_safe를 불러와 사용해야 입력값으로 html태그를 넣더라도 반영이됨
        # 보안의 문제로 django에서 html 태그 입력값은 반영되지 않게 막아놓음
        return mark_safe(f"<img width='70px' src={obj.file.url}>")

    get_thumbnail.short_description = "Thumbnail"
