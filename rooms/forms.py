from django import forms
from django_countries.fields import CountryField


from rooms import models as room_models


"""
    form api reference : https://docs.djangoproject.com/en/3.0/topics/forms/

"""


class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere",)
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(
        queryset=room_models.RoomType.objects.all(),
        required=False,
        empty_label="Any Kind",
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        queryset=room_models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    facilities = forms.ModelMultipleChoiceField(
        queryset=room_models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    pass
