from django.db import models

# Create your models here.
class Node(models.Model):
    node_ip = models.CharField(max_length=50)
    node_location = models.ForeignKey('Location', on_delete=models.CASCADE)

    verde = 0
    amarillo = 1
    rojo = 2
    STATES=(
    (verde, 'VERDE'),
    (amarillo, 'AMARILLO'),
    (rojo, 'ROJO')
    )
    node_states = models.CharField(max_length=1, choices=STATES)

class Location(models.Model):
    location_lat = models.DecimalField(max_digits=11, decimal_places = 7)
    location_lon = models.DecimalField(max_digits=11, decimal_places = 7)

class Node_status_records(models.Model):
    node = models.ForeignKey('Node', on_delete=models.CASCADE)
    record_date = models.DateTimeField(auto_now_add=True)
