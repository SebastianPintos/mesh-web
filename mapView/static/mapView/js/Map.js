var Map = function(divId){

	var map = L.map('meshMap')

	this.init = function(){
		L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
		  attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
		}).addTo(map);

		map.setView([-34.542229, -58.711903], 18);
	}

	this.addNode = function(node){
		node.marker.addTo(map)
	}

}