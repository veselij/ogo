from django.urls import path
from main.views import TripListView, TripDetailView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
        path('', TripListView.as_view(template_name='main/index.html'), name='main'),
        path('trip/<int:pk>/', TripDetailView.as_view(), name='trip_detail'),
        ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
