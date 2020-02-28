from django.urls import path
from . import views

app_name = "rooms"  # config/urls.py의 namespace와 같아야함.


urlpatterns = [
    path("<int:pk>", views.RoomDetail.as_view(), name="detail"),
    path("search/", views.SearchView.as_view(), name="search"),
]

