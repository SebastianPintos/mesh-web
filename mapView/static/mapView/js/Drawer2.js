var Drawer = function(canvasMap){

	this.canvasMap = canvasMap;

	this.draw = function(setOfNodes){
		if (! this._isThereAnyMarker()){
			setOfNodes.forEach(node => this._addMarkerToMap(node));
		}
		else
			setOfNodes.forEach(node => this._actualizeMarker(node));
	}

	_choseIconByState = function(nodeState){
		switch (nodeState){
			case 'VERDE': return greenIcon; break;
			case 'AMARILLO': return yellowIcon; break;
			default: return redIcon;
		}
	}

	_choseIconByHardware = function(nodeHardware){
		switch (nodeHardware){
			case 'UBIQUITY': return ubiquityIcon; break;
			case 'RASPBERRY': return raspberryIcon; break;
			default: return ubiquityIcon;
		}
	}

	this._addMarkerToMap = function(node){
		marker = L.marker([node.lat, node.lon]);
		marker.bindPopup("Ip = " + node.ip + "\n" + "Estado = " + node.state); //TODO Pone más lindo
		marker.title = node.ip;
		marker.setIcon(_choseIconByHardware(node.hardware));
		marker.addTo(canvasMap);//TODO cambiar
		markers.push(marker);
	}

	this._actualizeMarker = function(node){
		this.canvasMap.eachLayer(function(layer){
			if (layer.title === node.ip){
				layer.setIcon(_choseIconByHardware(node.hardware));
			}
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
			iconSize:     [100, 60], // size of the icon
			iconAnchor:   [18, 32], // point of the icon which will correspond to marker's location
			popupAnchor:  [23, -12] // point from which the popup should open relative to the iconAnchor
		})
	}
}
