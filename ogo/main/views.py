from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from main.models import Trip


class TripListView(ListView):
    """ View of all trips as table. """
    model = Trip
    context_object_name = 'trip_list'

    def get_queryset(self):
        """ Overrode method to filter by country name if search_query provided in request """
        search_query = self.request.GET.get('search_query')
        if search_query:
            print(search_query)
            return Trip.objects.filter(country__country__contains=search_query.lower())
        else:
            return Trip.objects.all()


class TripDetailView(DetailView):
    """ View of trip details. """
    model = Trip
