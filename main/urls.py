from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('admin_zone', views.zone_index),
    path('admin_extent', views.extent_index),
    path('plot', views.get_plot),
    path('plots', views.get_plots),
    path('measurements', views.data),
    path('zone/<int:id>', views.zone),
    path('apply-zone', views.apply_zone),
    path('points', views.points),
    path('zones', views.zones),
    path('extents', views.extents),
    path('privacy', views.privacy),
    path('about', views.about)
]
