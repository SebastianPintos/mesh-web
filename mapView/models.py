from django.db import models


# Create your models here.
class Node(models.Model):
    node_ip = models.CharField(max_length=50, primary_key=True)
    node_location = models.ForeignKey('Location', on_delete=models.CASCADE)

    verde = 0
    amarillo = 1
    rojo = 2

    STATES = (
        (verde, 'VERDE'),
        (amarillo, 'AMARILLO'),
        (rojo, 'ROJO')
    )
    node_states = models.CharField(max_length=20, choices=STATES, default=2)

    ubiquity_unify_outdoor_plus = 0
    raspberry_pi_3 = 1

    STATES2 = (
        (ubiquity_unify_outdoor_plus, 'UBIQUITY'),
        (raspberry_pi_3, 'RASPBERRY')
    )

    node_hardware = models.CharField(max_length=20, choices=STATES2, default='UBIQUITY')


class Location(models.Model):
    location_lat = models.DecimalField(max_digits=11, decimal_places=7)
    location_lon = models.DecimalField(max_digits=11, decimal_places=7)


class NodeLogCurrentRecords(models.Model):
    record_node = models.ForeignKey(Node, on_delete=models.CASCADE)
    record_date = models.DateTimeField(auto_now_add=True)
    record_electric_current = models.DecimalField(max_digits=10, decimal_places=8)

class NodeLogTemperatureRecords(models.Model):
    record_node = models.ForeignKey(Node, on_delete=models.CASCADE)
    record_date = models.DateTimeField(auto_now_add=True)
    record_temperature = models.DecimalField(max_digits=10, decimal_places=8)

class UdpPackage:
    def __init__(self, type, ip, timestamp, values):
        self.type = type
        self.ip = ip
        self.timestamp = timestamp
        self.values = values
