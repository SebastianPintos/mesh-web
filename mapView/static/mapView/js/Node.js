var Node = function(latLng, ip, state){

	this.latlng = latLng;
	this.currentState = state;
	this.ip = ip;
}

function isServerDown(serverStat){
	if (serverStatus === "up" && serverStat === "down")
		return true
	return false
}

function saveCluster(jsonCluster){
	jsonCluster.map(nodeJson => function(nodeJson){
		markerToAdd = L.marker([nodeJson.lat, nodeJson.lon]);
		markerToAdd.title = nodeJson.ip;
	})
}

function parseStringToJSONObject(jsonstring){
	return JSON.parse(jsonstring);
}
