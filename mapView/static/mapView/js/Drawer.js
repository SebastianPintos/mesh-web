var Drawer = function(canvasMap){

	this.canvasMap = canvasMap;

	this.draw = function(setOfNodes){
		if (! this._isThereAnyMarker()){
			setOfNodes.forEach(node => this._addMarkerToMap(node));
		}
		else
			setOfNodes.forEach(node => this._actualizeMarker(node));
	}

	this.alertChanges = function(serverStat){
		if (isServerDown(serverStat))
			alert("Advertencia, el server está caído")
		serverStatus = serverStat;
	}

	_choseIconByState = function(nodeState){
		switch (nodeState){
			case 'VERDE': return greenIcon; break;
			case 'AMARILLO': return yellowIcon; break;
			case 'VIOLETA': return violetIcon; break;
			default: return redIcon;
		}
	}

	this._addMarkerToMap = function(node){
		marker = L.marker([node.lat, node.lon]);
		marker.bindPopup("Ip = " + node.ip); //TODO Pone más lindo
		marker.title = node.ip;
		marker.setIcon(_choseIconByState(node.state));
		marker.addTo(canvasMap);//TODO cambiar
		markers.push(marker);
	}

	this._actualizeMarker = function(node){
		this.canvasMap.eachLayer(function(layer){
			if (layer.title === node.ip)
				layer.setIcon(_choseIconByState(node.state));
		})
	}

	this._isThereAnyMarker = function(){
		retValue = false;
		markers.forEach(marker => retValue |= this.canvasMap.hasLayer(marker));
		return retValue;
	}

	this.createIcon = function(filePath){
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
