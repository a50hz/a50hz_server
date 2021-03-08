from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('admin_zone', views.cooler_index),
    path('plot', views.get_plot),
    path('measurements', views.data),
    path('zone', views.zone),
    path('points', views.points),
    path('zones', views.zones),
    path('privacy', views.privacy),
    path('about', views.about)
]