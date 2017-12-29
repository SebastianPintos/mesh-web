var map = new Map("meshMap");
map.init();

$.when($.ajax('http://localhost:8000/mapView/get-info')). //Request a Django
then(response => parseStringToJSONObject(response)). //Response con JSON String a Object
then(jsonCluster => getCluster(jsonCluster)). //obtengo una lista de nodos
done(cluster => cluster.map(node => map.addNode(node))); //los dibujo en el mapa

