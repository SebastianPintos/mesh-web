from django.core.serializers import serialize
import json
from mapView.models import Node, Location


def get_nodes():
    return Node.objects.all()


def get_json_from_models(nodes):  # TODO cambiar nombre
    to_ret = []
    for node in nodes:
        node_to_add = NodeMapper(node)
        to_ret.append(node_to_add.__dict__)
    return json.dumps(to_ret)

class NodeMapper:
    def __init__(self, node):
        self.ip = node.node_ip
        self.state = node.node_states
        self.lat = node.node_location.location_lat.__float__()
        self.lon = node.node_location.location_lon.__float__()





