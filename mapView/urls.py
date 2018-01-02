from django.urls import path
from mapView.retrieve_info import retrieve_info_daemon

from . import views

urlpatterns = [
    path('map', views.map, name='map'),
    path('', views.index, name='index'),
    path('get-info', views.node_info, name='get info')
]

#Start up deamons
retrieve_info_daemon()
