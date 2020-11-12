from django.contrib.gis.db import models


# Create your models here.
class Measurement(models.Model):
    class Meta:
        db_table = "measurement"
    data = models.IntegerField()
    location = models.PointField()
    time = models.TimeField()