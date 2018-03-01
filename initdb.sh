#!/bin/bash
python3 manage.py shell --command="
from mapView.models import Node, Location, NodeLogCurrentRecords

masterNodeLoc =  Location(location_lat=-34.543327, location_lon=-58.711582)
masterNodeLoc.save()
masterNode = Node(node_ip = '10.10.5.5', node_location=masterNodeLoc, node_states = 'ROJO', node_hardware = 'UBIQUITY')
masterNode.save()

clientNode1Loc =  Location(location_lat=-34.542848, location_lon=-58.712592)
clientNode1Loc.save()
clientNode1 = Node(node_ip = '10.10.5.1', node_location=clientNode1Loc, node_states = 'ROJO', node_hardware = 'UBIQUITY')
clientNode1.save()

clientNode2Loc =  Location(location_lat=-34.542606, location_lon=-58.711649)
clientNode2Loc.save()
clientNode2 = Node(node_ip = '10.10.5.2', node_location=clientNode2Loc, node_states = 'ROJO', node_hardware = 'UBIQUITY')
clientNode2.save()

clientNode3Loc =  Location(location_lat=-34.543245, location_lon=-58.712421)
clientNode3Loc.save()
clientNode3 = Node(node_ip = '10.10.5.3', node_location=clientNode3Loc, node_states = 'ROJO', node_hardware = 'RASPBERRY')
clientNode3.save()

clientNode4Loc =  Location(location_lat=-34.542982, location_lon=-58.712756)
clientNode4Loc.save()
clientNode4 = Node(node_ip = '10.10.5.4', node_location=clientNode4Loc, node_states = 'ROJO', node_hardware = 'UBIQUITY')
clientNode4.save()

log1 = NodeLogCurrentRecords(record_node = clientNode1, record_electric_current=0)
log2 = NodeLogCurrentRecords(record_node = clientNode2, record_electric_current=0)
log3 = NodeLogCurrentRecords(record_node = clientNode3, record_electric_current=0)
log4 = NodeLogCurrentRecords(record_node = clientNode4, record_electric_current=0)

logM.save()
log1.save()
log2.save()
log3.save()
log4.save()

"
