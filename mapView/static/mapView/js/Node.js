var Node = function(latLng, ip, state){

	this.currentState = state;	
	this.ip = ip;

	this.marker = L.marker(latLng);
	this.marker.bindPopup("Ip = " + ip); //TODO Pone más lindo
}

function getCluster(){
	//Esta función se comunicaría con Django
	var node1 = new Node([-34.542362, -58.712332], "10.10.5.1", "GRIS");
	var node2 = new Node([-34.542606, -58.711649], "10.10.5.2", "GRIS");
	var node3 = new Node([-34.543245, -58.712421], "10.10.5.3", "GRIS");
	var node4 = new Node([-34.542982, -58.712756], "10.10.5.4", "GRIS");

	return [node1, node2, node3, node4];
}