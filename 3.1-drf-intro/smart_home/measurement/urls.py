from smart_home.settings import DEBUG, MEDIA_URL, MEDIA_ROOT
from django.urls import path, include
from django.conf.urls.static import static
from PIL import Image

from measurement.views import SensorListAPIView, SensorAPIView, photo_view

urlpatterns = [
    path('sensors/', SensorListAPIView.as_view()),
    path('sensors/<pk>/', SensorAPIView.as_view()),
    path('measurements/', SensorAPIView.as_view()),
    path('media/<filename>/', photo_view),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
