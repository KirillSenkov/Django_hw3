# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView

from django.db import connection
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import  Response
from rest_framework import status
from .models import Sensor, Measurement
from .serializers import SensorSerializer, SensorDetailSerializer, \
    MeasurementSerializer
from PIL import Image
from rest_framework.parsers import JSONParser, FileUploadParser, \
    MultiPartParser, FormParser

class SensorListAPIView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        Sensor.objects.all().delete()
        with connection.cursor() as cur:
            cur.execute(
                "ALTER SEQUENCE measurement_sensor_id_seq RESTART WITH 1;")
        return Response({"message": "All sensors deleted"},
                        status=status.HTTP_204_NO_CONTENT)

class SensorAPIView(RetrieveAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        sensor_id = request.data.get('sensor')
        temperature = request.data.get('temperature')
        photo = request.data.get('photo')

        if not sensor_id or not temperature:
            return Response({"error": "Sensor ID and temperature are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        sensor = get_object_or_404(Sensor, id=sensor_id)

        try:
            sensor.post_measurement(temperature, photo)
            return Response({"message": "Measurement recorded successfully."},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def patch(self, request, pk, *args, **kwargs):
        sensor = get_object_or_404(Sensor, id=pk)

        if 'description' in request.data:
            sensor.description = request.data['description']
            sensor.save()
            return Response({"message": "Description updated", "description": sensor.description}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No description provided"}, status=status.HTTP_400_BAD_REQUEST)


def photo_view(request, filename):
    measurement = get_object_or_404(Measurement, photo=filename)
    photo_path = measurement.photo.path

    if os.path.exists(photo_path):
        with open(photo_path, 'rb') as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    else:
        raise Http404("Image not found")