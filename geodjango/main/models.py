from django.contrib.gis.db import models


# Create your models here.
class Measurement(models.Model):
    data = models.IntegerField()
    location = models.PointField()
    time = models.TimeField()

    def __str__(self):
        return 'ID: {}\n'.format(self.id)