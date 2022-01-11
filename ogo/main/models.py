from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    """ Base model for create and update fields. """

    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    updated = models.DateTimeField(auto_now=True, help_text='Дата изменения')


class Customer(models.Model):
    """ Customer class extends django User. """
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text='Клиент')
    mobile_phone_number = models.CharField(max_length=12, help_text='в формате +7ХХХХХХХХХХ')

    def __str__(self) -> str:
        return self.user.username


class Country(models.Model):
    """ Model for trip country field. """
    country = models.CharField(max_length=100, help_text='Страна путешествия')

    def __str__(self):
        return self.country


class PurchasedTrip(BaseModel):
    """ Model for trips purchased by customers. """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, help_text='Клиент')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, help_text='Страна путевки')
    start_date = models.DateField(help_text='Дата начала путевки')
    purchased_date = models.DateField(help_text='Дата покупки')
    amount = models.FloatField(help_text='Сумма путевки')
    hotel = models.CharField(max_length=100, help_text='Отель')
    comment = models.CharField(max_length=100, help_text='Комментарий')

    def __str__(self):
        return f'{self.customer} {self.hotel}'


class Trip(BaseModel):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, help_text='Страна путевки')
    price = models.FloatField(help_text='Цена')
    description = models.TextField(help_text='Описание предложения')

    def __str__(self):
        return self.description

def trip_path(instance, filename):
    return f'{instance.trip.name}/{filename}'

class Picture(BaseModel):
    """ Model for storing images for trips. """
    pictrure = models.ImageField(upload_to=trip_path)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, help_text='Путевка')
