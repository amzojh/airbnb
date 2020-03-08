from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField


from core import models as core_models
from users import models as user_models

# Create your models here.


class AbstractItem(core_models.TimeStampedModel):

    """ Abstraft Item Definition"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    """ Room type Definition"""

    class Meta:
        verbose_name = "Room Types"

    pass


class Amenity(AbstractItem):

    """ Amenity Item """

    class Meta:
        verbose_name_plural = "Amenities"

    pass


class Facility(AbstractItem):

    """ Facility Item Definition """

    class Meta:
        verbose_name_plural = "Facilities"

    pass


class HouseRule(AbstractItem):

    """ HouseRule Item Definition """

    class Meta:
        verbose_name = "House Rules"

    pass


class Room(core_models.TimeStampedModel):

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    guests = models.IntegerField()
    check_in = models.TimeField()  # 0 ~ 24 only for hours
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)

    # related_name은 Target(user_models.User)를 위한 것이며, 생성되는 {objectname}_set에 대한 이름을 바꾸는 것임
    host = models.ForeignKey(
        user_models.User, related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        RoomType, related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField(Amenity, related_name="rooms", blank=True)
    facilities = models.ManyToManyField(Facility, related_name="rooms", blank=True)
    house_rules = models.ManyToManyField(HouseRule, related_name="rooms", blank=True)

    # reference : https://docs.djangoproject.com/en/3.0/topics/db/models/
    # self.obj 를 통해서 유효성검사를 해주면된다.
    def save(self, *args, **kargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kargs)
        pass

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})  # urls의 namespace및 name

    def __str__(self):
        return self.name

    def total_rating(self):
        # review에 many to many로 엮여있기 때문에, self.review로 접근이 가능함.
        all_reviews = self.review.all()
        all_ratings = 0

        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 2)
        return 0

    def first_photo(self):
        (photo,) = self.photos.all()[:1]
        return photo.file.url


class Photo(core_models.TimeStampedModel):

    """ Photo Item Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey(Room, related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.caption}'s photo"

    pass
