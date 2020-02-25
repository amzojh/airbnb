from django.urls import path
from . import views

app_name = "rooms"  # config/urls.py의 namespace와 같아야함.


urlpatterns = [
    path(
        "<int:pk>", views.RoomDetail.as_view(), name="detail"
    ),  # 해당 path의 경우, namespace:name 으로 접근이 가능함.
    path("search/", views.search, name="search"),
]

