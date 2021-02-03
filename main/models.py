from django.db import models

# Create your models here.
class Measurement(models.Model):
    data = models.DecimalField(max_digits=7, decimal_places=2)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    date_time = models.DateTimeField()

    def __str__(self):
        return '{}'.format(self.id)


class Extent(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    place = models.fields.CharField(max_length=428)
    x1 = models.DecimalField(max_digits=17, decimal_places=14)
    x2 = models.DecimalField(max_digits=17, decimal_places=14)
    y1 = models.DecimalField(max_digits=17, decimal_places=14)
    y2 = models.DecimalField(max_digits=17, decimal_places=14)
    zoom = models.DecimalField(max_digits=7, decimal_places=5)

    def __str__(self):
        return '{}'.format(self.id)


class Plot(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    value = models.fields.TextField()
    date = models.DateTimeField()
    type = models.fields.CharField(max_length=50)
    interpolation_type = models.fields.CharField(max_length=50)
    extentId = models.BigIntegerField(serialize=False)

    def __str__(self):
        return '{}'.format(self.id)