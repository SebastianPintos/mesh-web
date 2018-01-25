var Node = function(latLng, ip, state){

	this.latlng = latLng;
	this.currentState = state;
	this.ip = ip;
}

/*function saveCluster(jsonCluster){
	nodes = [];
	jsonCluster.map(nodeJson => nodes.push(new Node([nodeJson.lat, nodeJson.lon],
														nodeJson.ip,
														nodeJson.state)));
}*/

function saveCluster(jsonCluster){
	jsonCluster.map(nodeJson => function(nodeJson){
		markerToAdd = L.marker([nodeJson.lat, nodeJson.lon]);
		markerToAdd.title = nodeJson.ip;


	})
}

function parseStringToJSONObject(jsonstring){
	return JSON.parse(jsonstring);
}
