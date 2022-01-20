from django.contrib import admin
from main.models import Customer, Country, PurchasedTrip, Trip, Picture, Seller, Resort


admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(Resort)
admin.site.register(Country)
admin.site.register(PurchasedTrip)
admin.site.register(Trip)
admin.site.register(Picture)
