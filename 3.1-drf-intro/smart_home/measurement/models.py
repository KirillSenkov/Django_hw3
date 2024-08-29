from django.db import models
from django.core.validators import MinValueValidator
from PIL import Image

class Sensor(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=1000,
                                   verbose_name='Описание',
                                   blank=True, null=True)

    def post_measurement(self, temperature, photo):
        try:

            measurement = Measurement(sensor_id=self,
                                      temperature=temperature,
                                      photo=photo)
            if photo:
                print(f'type(measurement.photo)>{type(measurement.photo)}<'
                      f'measurement.photo.size>{measurement.photo.size}<'
                      f'measurement.photo.name>{measurement.photo.name}<')
            measurement.save()

        except Exception as e:
            raise ValueError(f'Sensor.post_measurement(>{self.id}<, '
                             f'>{temperature}<) error: '
                             f'{str(e)}')


class Measurement(models.Model):
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE,
                                  verbose_name='ID датчика',
                                  related_name='measurements')
    temperature = models.FloatField(validators=[MinValueValidator(-273)],
                                    verbose_name='Температура при ' \
                                                    'измерении')
    photo = models.ImageField(verbose_name='Фото', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата и время измерения')

