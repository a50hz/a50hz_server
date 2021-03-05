from django.db import models
import django.utils.timezone 

# Create your models here.
class Measurement(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    data = models.DecimalField(max_digits=7, decimal_places=2)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    date_time = models.DateTimeField()

    def __str__(self):
        return '{}'.format(self.id)


class Extent(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    place = models.fields.CharField(max_length=428)
    lat1 = models.DecimalField(max_digits=19, decimal_places=17, null=True)
    lat2 = models.DecimalField(max_digits=19, decimal_places=17, null=True)
    lng1 = models.DecimalField(max_digits=20, decimal_places=18, null=True)
    lng2 = models.DecimalField(max_digits=20, decimal_places=18, null=True)
    zoom = models.DecimalField(max_digits=7, decimal_places=5, null=True)

    def get_center(self):
        return ((self.x2 - self.x1) / 2, (self.y2 - self.y1) / 2)

    
    def __str__(self):
        return '{}'.format(self.id)


class Plot(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    value = models.fields.BinaryField()
    date = models.DateTimeField(default=django.utils.timezone.now)
    kind = models.fields.CharField(max_length=50)
    interpolation_type = models.fields.CharField(max_length=50)
    Extent = models.ForeignKey(Extent, on_delete=models.DO_NOTHING)

    def __str__(self):
        return '{}'.format(self.id)


class ResearchZone(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.fields.CharField(max_length=428)
    lat1 = models.DecimalField(max_digits=19, decimal_places=17, null=True)
    lng1 = models.DecimalField(max_digits=20, decimal_places=18, null=True)
    lat2 = models.DecimalField(max_digits=19, decimal_places=17, null=True)
    lng2 = models.DecimalField(max_digits=20, decimal_places=18, null=True)

    def __str__(self):
        return '{}'.format(self.id)