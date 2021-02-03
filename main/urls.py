from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('measurements', views.data),
    path('isolines', views.get_isolines),
    path('heatmap', views.get_heatmap),
    path('about', views.about),
    path('style.css', views.style),
    path('scripts.js', views.scripts),
    path('privacy', views.privacy)
]