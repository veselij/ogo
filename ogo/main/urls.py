from django.urls import path
from main.views import TripListView, TripDetailView, TripCreateView, TripUpdateView, AboutTemplateView, ContactTeplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
        path('', TripListView.as_view(template_name='main/index.html'), name='main'),
        path('about/', AboutTemplateView.as_view(), name='about'),
        path('contacts/', ContactTeplateView.as_view(), name='contacts'),
        path('trip/<slug:slug>/', TripDetailView.as_view(), name='trip_detail'),
        path('trip/add/', TripCreateView.as_view(), name='trip_add'),
        path('trip/<pk:int>/edit/', TripUpdateView.as_view(), name='trip_edit'),
        ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
