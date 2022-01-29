from django.contrib import sitemaps
from django.urls import reverse
from main.models import Trip
from django.contrib.sitemaps import GenericSitemap


class StaticSiteMap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['main', 'about', 'contacts']

    def location(self, obj: str):
        return reverse(obj)


trip_dict = {
        'queryset': Trip.top_objects.all(),
        'date_field': 'updated',
        }

sitemaps = {'static': StaticSiteMap, 'trip': GenericSitemap(trip_dict, priority=0.6)}
