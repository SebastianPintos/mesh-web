from django.urls import path

from . import views

urlpatterns = [
    path('<int:node_name>/', views.want_see, name='Node Name'),
    path('map', views.map, name='map'),
    path('', views.index, name='index'),
]
