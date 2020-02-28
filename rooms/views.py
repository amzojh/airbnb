from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.urls import reverse
from django.http import Http404
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django_countries import countries

from rooms import models as room_models
from rooms import forms as room_forms

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


class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")
        filter_args = {}

        if country:
            form = room_forms.SearchForm(request.GET)

            if form.is_valid():

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")
                print(facilities)

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                qs = room_models.Room.objects.filter(**filter_args).order_by("-created")

                for amenity in amenities:
                    rooms = qs.filter(amenities__pk=amenity.pk)

                for facility in facilities:
                    rooms = qs.filter(facilities__pk=facility.pk)

                paginator = Paginator(qs, 10, orphans=5)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)

                return render(
                    request,
                    "rooms/room_search.html",
                    context={"form": form, "rooms": rooms},
                )

        else:
            form = room_forms.SearchForm

        return render(request, "rooms/room_search.html", context={"form": form})


"""
1. config/urls.py
2. rooms/urls.py (pattern : rooms/{int:pk})
3. room_detail(request, pk)

"""

"""
input tag : https://yangbari.tistory.com/28
django_fieldlookup
"""


def search(request):
    form = None
    country = request.GET.get("country")
    filter_args = {}

    if country:
        form = room_forms.SearchForm(request.GET)

        if form.is_valid():

            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            price = form.cleaned_data.get("price")
            guests = form.cleaned_data.get("guests")
            bedrooms = form.cleaned_data.get("bedrooms")
            beds = form.cleaned_data.get("beds")
            baths = form.cleaned_data.get("baths")
            instant_book = form.cleaned_data.get("instant_book")
            superhost = form.cleaned_data.get("superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")
            print(facilities)

            if city != "Anywhere":
                filter_args["city__startswith"] = city

            filter_args["country"] = country

            if room_type is not None:
                filter_args["room_type"] = room_type

            if price is not None:
                filter_args["price__lte"] = price

            if guests is not None:
                filter_args["guests__gte"] = guests

            if bedrooms is not None:
                filter_args["bedrooms__gte"] = bedrooms

            if beds is not None:
                filter_args["beds__gte"] = beds

            if baths is not None:
                filter_args["baths__gte"] = baths

            if instant_book is True:
                filter_args["instant_book"] = True

            if superhost is True:
                filter_args["host__superhost"] = True

            if amenities is not None:
                filter_args["amenities"] = amenities

            if facilities is not None:
                filter_args["facilities"] = facilities

    else:
        form = room_forms.SearchForm

    print(filter_args)

    rooms = room_models.Room.objects.filter(**filter_args)

    return render(
        request, "rooms/room_search.html", context={"form": form, "rooms": rooms}
    )


def room_detail(request, pk):
    try:
        room = room_models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"room": room})
    except room_models.Room.DoseNotExist:
        raise Http404("")
