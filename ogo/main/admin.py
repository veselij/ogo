from django.contrib import admin
from main.models import Customer, Country, PurchasedTrip, Trip, Picture, Seller, Resort


class TripAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated',  'start_date', 'slug')
    list_filter = ('resort__country', )
    search_fields = ('name', )


admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(Resort)
admin.site.register(Country)
admin.site.register(PurchasedTrip)
admin.site.register(Trip, TripAdmin)
admin.site.register(Picture)
