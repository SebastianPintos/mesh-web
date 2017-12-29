from django.urls import path

from . import views

urlpatterns = [
    path('map', views.map, name='map'),
    path('', views.index, name='index'),
    path('get-info', views.node_info, name='get info')
]
