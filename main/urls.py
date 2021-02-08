from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('plot', views.get_plot),
    path('measurements', views.data),
    path('update', views.update),
    path('privacy', views.privacy),
    path('about', views.about)
]