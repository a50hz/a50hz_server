from django.db import models

# Create your models here.
class Measurement(models.Model):
    data = models.IntegerField()
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    date_time = models.DateTimeField()

    def __str__(self):
        return '{}'.format(self.id)