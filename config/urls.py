"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rooms import views as room_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("rooms/", include("rooms.urls", namespace="rooms")),
    path("", include("core.urls", namespace="core")),
]


# URL경로와 우리의 DIR경로가 꼭 같을 필요는 없음. 이렇게 MEDIA라고하는 folder루트에 MEDIA_ROOT를 추가해주어도됨.

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
