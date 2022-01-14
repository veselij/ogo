from django.forms import ModelForm, inlineformset_factory
from main.models import Trip, Picture


class TripForm(ModelForm):
    """ Form to create trips. """
    class Meta:
        model = Trip
        fields = '__all__'

ImageFormset = inlineformset_factory(Trip, Picture, fields=('picture', 'front_picture' ), extra=5)
