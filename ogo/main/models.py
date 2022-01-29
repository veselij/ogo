from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class TopTripManager(models.Manager):
    """ Trip manager - returns last 50 created trips. """
    def get_queryset(self):
        return super().get_queryset().order_by('-created')[:50]


class BaseModel(models.Model):
    """ Base model for create and update fields. """

    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True, help_text='Дата создания')
    updated = models.DateTimeField(auto_now=True, help_text='Дата изменения')


class Seller(models.Model):
    """ Sales manager. """
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text='Менеджер по продажам')
    mobile_phone_number = models.CharField(max_length=11, help_text='в формате 7ХХХХХХХХХХ')

    def __str__(self) -> str:
        return self.user.username


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

class Resort(models.Model):
    """ Model for resort region. """
    resort = models.CharField(max_length=100, help_text='Курорт')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.resort

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
    
    class Meta:
        ordering = ('-id', )

    name = models.CharField(max_length=100)
    price = models.FloatField(help_text='Цена')
    description = models.TextField(help_text='Корткое описание предложения')
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE, help_text='Курорт')
    beach = models.CharField(max_length=255, default='', help_text='Пляжная линия')
    start_date = models.DateField(help_text='Дата заезда')
    duration = models.IntegerField(help_text='Длительность тура')
    meal_type = models.CharField(max_length=255, default='', help_text='Тип питания')
    stars = models.IntegerField(default=-1, help_text='Звезды')
    lat = models.FloatField(default=0, null=True, help_text='latitude')
    long = models.FloatField(default=0, null=True, help_text='longitude')
    room_type = models.CharField(max_length=255, default='', help_text='Тип номера')
    slug = models.SlugField(null=False, unique=True)

    objects = models.Manager()
    top_objects = TopTripManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('trip_detail', kwargs={'slug' : self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.name}{self.start_date}')
        return super().save(*args, **kwargs)

def trip_path(instance, filename):
    return f'{instance.trip.name}/{filename}'

class Picture(BaseModel):
    """ Model for storing images for trips. """
    picture = models.ImageField(upload_to=trip_path, blank=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, help_text='Путевка')
    front_picture = models.BooleanField(default=False, help_text='Главная картинка')

    def __str__(self):
        return self.trip.name

