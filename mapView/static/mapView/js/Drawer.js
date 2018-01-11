var Drawer = function(canvasMap){

	this.canvasMap = canvasMap;

	this.draw = function(){
		if (! this._isThereAnyMarker()){
			nodes.forEach(node => this._addMarkerToMap(node));
		}
		else
			nodes.forEach(node => this._actualizeMarker(node));
	}

	this._choseIconByState = function(nodeState){
		switch (nodeState){
			case 'VERDE': return greenIcon; break;
			case 'AMARILLO': return yellowIcon; break;
			default: return redIcon;
		}
	}

	this._addMarkerToMap = function(node){
		marker = L.marker(node.latlng);
		marker.bindPopup("Ip = " + node.ip); //TODO Pone más lindo
		marker.title = node.ip;
		marker.setIcon(this._choseIconByState(node.currentState));
		marker.addTo(canvasMap);//TODO cambiar

	}

	this._actualizeMarker = function(node){
		this.canvasMap.eachLayer(function(layer){
			if (layer.title === node.ip)
				layer.setIcon(this._choseIconByState(node.nodeState));
		})
	}

	this._isThereAnyMarker = function(){
		return false;
	}

	this.createIcon = function(filePath){
		console.log(filePath);
		return icon = L.icon({
			iconUrl: filePath,
			iconSize:     [35, 35], // size of the icon
		//	shadowSize:   [50, 64], // size of the shadow
			iconAnchor:   [18, 32], // point of the icon which will correspond to marker's location
		//	shadowAnchor: [4, 62],  // the same for the shadow
			popupAnchor:  [0, -25] // point from which the popup should open relative to the iconAnchor
		})
	}
}

