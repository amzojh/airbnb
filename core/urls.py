from django.urls import path
from rooms import views as room_views

app_name = "core"  # 반드시 붙여주어야함.

urlpatterns = [path("", room_views.HomeView.as_view(), name="home")]
