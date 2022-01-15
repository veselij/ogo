from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import Trip, Country, Seller
from main.forms import TripForm, ImageFormset


class CountryMixin(object):
    """ Mixin to add county in views. """
    def get_context_data(self, **kwargs):
        """ Overiding defautl method to get also list of countries """
        context = super(CountryMixin, self).get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        context['seller'] = Seller.objects.first()
        return context


class AboutTemplateView(CountryMixin, TemplateView):
    template_name = 'about.html'


class ContactTeplateView(CountryMixin, TemplateView):
    template_name = 'contacts.html'


class TripListView(CountryMixin, ListView):
    """ View of all trips as table. """
    model = Trip
    context_object_name = 'trip_list'

    def get_queryset(self):
        """ Overrode method to filter by country name if search_query provided in request """
        search_query = self.request.GET.get('search_query')
        if search_query:
            return Trip.objects.filter(country__country=search_query)
        else:
            return Trip.objects.all()


class TripDetailView(CountryMixin, DetailView):
    """ View of trip details. """
    model = Trip


class TripCreateView(LoginRequiredMixin, CreateView):
    """ View to add Trips with pictures. """
    model = Trip
    template_name_suffix = '_add_form'
    form_class = TripForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formset = ImageFormset()
        context['formset'] = formset
        return context

    def post(self, *args, **kwargs):
        form = self.get_form()
        self.object = None
        if form.is_valid():
            self.object = form.save()
            picture = ImageFormset(self.request.POST, self.request.FILES, instance=self.object)
            if picture.is_valid():
                picture.save()
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)


class TripUpdateView(LoginRequiredMixin, UpdateView):
    """ View to edit trips. """
    model = Trip
    template_name_suffix = '_edit_form'
    form_class = TripForm
    picture_form = ImageFormset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formset = ImageFormset(instance=self.object)
        context['formset'] = formset
        return context

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            self.object = form.save()
            picture = ImageFormset(self.request.POST, self.request.FILES, instance=self.object)
            if picture.is_valid():
                picture.save()
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)
