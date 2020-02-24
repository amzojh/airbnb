from django.contrib import admin
from django.utils.html import mark_safe

from . import models


# Register your models here.
@admin.register(models.RoomType, models.Facility, models.HouseRule, models.Amenity)
class ItemAdmin(admin.ModelAdmin):

    list_display = ["name", "used_by"]

    def used_by(self, obj):
        return obj.rooms.count()

    """ Item Admin Definition """

    pass


class PhotoInline(admin.TabularInline):
    """ Photo Inline Definition
        해당 class 덕분에 admin 패널 안에 Foreinkey로 엮인 admin 패널까지 보여줄 수 있음.

    """

    model = models.Photo
    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    inlines = (PhotoInline,)

    """ Room admin Definition"""

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")},),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms")},),
        (
            "More About the Space",
            {"fields": ("amenities", "facilities", "house_rules")},
        ),
        ("Last Details", {"fields": ("host",)},),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "beds",
        "bedrooms",
        "baths",
        "guests",
        "instant_book",
        "count_amenities",
        "count_photos",
    )

    list_filter = [
        "instant_book",
        "host__superhost",
        "host__gender",
        "room_type",
        "facilities",
        "house_rules",
        "amenities",
        "city",
        "country",
    ]

    """
    reference : https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.filter_horizontal 
    """

    # ordering = ()

    """
    reference : https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.filter_horizontal 
    """

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    """
    reference : https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields
    
    Prefix	Lookup
    ^	startswith
    =	iexact
    @	search
    None	icontains    
    """
    search_fields = ["city", "^host__username"]

    raw_id_fields = ("host",)

    """
    self : 현재 class
    obj : 각 행들이 obj로 들어옴.
    """

    # admin을 컨트롤함.

    def save_model(self, request, obj, form, change):
        # send_mail() <- 어떤애가 바꾸려고하는지 intercept가 가능함.
        super().save_model(request, obj, form, change)
        pass

    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()

    pass


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo admin Definition"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="200px" src="{obj.file.url}"/>')

    get_thumbnail.short_description = "Thumbnail"

    pass

