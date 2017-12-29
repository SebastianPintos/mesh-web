var NodeMarker = function(latLng, ip, state){

	this.currentState = state;	
	this.ip = ip;

	this.marker = L.marker(latLng);
	this.marker.bindPopup("Ip = " + ip + "\n" + "Estado = " + state); //TODO Pone más lindo
}

function getCluster(jsonCluster){
	listToRet = [];

	jsonCluster.map(nodeJson => listToRet.push(new NodeMarker([nodeJson.lat, nodeJson.lon],
														nodeJson.ip,
														nodeJson.state)));
	return listToRet;
}

function parseStringToJSONObject(jsonstring){
	return JSON.parse(jsonstring);
}

