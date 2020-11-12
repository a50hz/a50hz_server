from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('measurements', views.data),
    path('get_data/', views.get_data),
    path('about', views.about)
]