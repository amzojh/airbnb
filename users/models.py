from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):

    """ Custom User model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, "English"), (LANGUAGE_KOREAN, "Korean"))

    CURRENCY_ENGLISH = "usd"
    CURRENCY_KOREAN = "krw"

    CURRENCY_CHOICES = (
        (CURRENCY_ENGLISH, "USD"),
        (CURRENCY_KOREAN, "KRW"),
    )

    avatar = models.ImageField(blank=True, upload_to="avatars")

    # null은 database에 영향을 주고, blank는 admin form에 영향을 준다.
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    bio = models.TextField(default="", null=True, blank=True)
    # 만약 기존User Table에 row가 생성되어있고 이렇게 bio라고하는 새로운 애를 추가하는 경우 혹은 default값을 알려줘야한다.

    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(blank=True, max_length=2, choices=LANGUAGE_CHOICES)
    currency = models.CharField(blank=True, max_length=3, choices=CURRENCY_CHOICES)
    superhost = models.BooleanField(default=False)
    pass
