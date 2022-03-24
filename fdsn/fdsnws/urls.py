from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('dataselect/', views.dataselect, name='dataselect'),
    path('station/', views.station, name='station'),
]
