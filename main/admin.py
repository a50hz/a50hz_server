from django.contrib import admin
from .models import Measurement, Plot, Extent, ResearchZone
# Register your models here.


admin.site.register(Measurement)
admin.site.register(Plot)
admin.site.register(Extent)
admin.site.register(ResearchZone)