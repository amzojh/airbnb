from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.urls import reverse
from django.http import Http404
from django.shortcuts import render, redirect
from rooms import models as room_models

# Create your views here.
# list view에서는 model, queryset 등을 정의해주어야 한다.


""" 
    Query limit
    Reference : https://docs.djangoproject.com/en/3.0/topics/db/queries/
    paginator.get_page(exception 처리X) vs page(exception 처리)
"""

"""
    class based view : https://ccbv.co.uk/
"""


class HomeView(ListView):
    """ Homeview Definition """

    model = room_models.Room
    paginate_by = 10
    paginate_orphans = 5
    context_object_name = "rooms"

    # get_context_data에서 context를 추가해줄 수 있음.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context

    pass


# 404 page로 바로 보내버림..
class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = room_models.Room
    pk_url_kwarg = "pk"  # pk_url_kwargs의 이름명에 따라서, urls.py에 정의된 pk 변수명이 달라져야함.

    pass


"""
1. config/urls.py
2. rooms/urls.py (pattern : rooms/{int:pk})
3. room_detail(request, pk)

"""


def search(request):
    city = str.capitalize(request.GET.get("city"))

    return render(request, "rooms/room_search.html", context={"city": city,})


def room_detail(request, pk):
    try:
        room = room_models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"room": room})
    except room_models.Room.DoseNotExist:
        raise Http404("")
