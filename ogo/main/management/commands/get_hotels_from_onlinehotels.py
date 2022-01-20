from django.core.management.base import BaseCommand
from main.models import Country, Picture, Trip, Resort
from main.parser import collect_data
import os
import requests
from io import BytesIO
import time


class Command(BaseCommand):
    help = 'Parse hot tours from onlinetpurs.ru'

    def add_arguments(self, parser):
        parser.add_argument('resort', nargs='+', type=str)

    def handle(self, *args, **options):
        resort = options['resort'][0]
        hotels = collect_data(resort)
        for hotel in hotels:
            country_name = hotel.short_location.split(',')[0]
            resort_name = hotel.short_location.split(',')[1]
            country, _ = Country.objects.get_or_create(country=country_name)
            resort, _ = Resort.objects.get_or_create(resort=resort_name, country=country)
            trip, _ = Trip.objects.get_or_create(name=hotel.hotel_name, price=hotel.price, description=hotel.description,
                    resort=resort, beach=hotel.beach, start_date=hotel.start_date, duration=hotel.duration, meal_type=hotel.meal_type,
                    stars=hotel.stars, lat=hotel.lat, long=hotel.long, room_type=hotel.room_type)
            for i, url in enumerate(hotel.images):
                time.sleep(1)
                response = requests.get(url).content
                pic = Picture.objects.create(trip=trip)
                pic.picture.save(os.path.basename(url), BytesIO(response))
                if i ==0:
                    pic.front_picture = True
                pic.save()
