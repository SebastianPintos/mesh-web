var requestInfo =  function(){
	$.when($.ajax('http://localhost:8000/mapView/get-info')). //Request a Django
	then(response => parseStringToJSONObject(response)). //Response con JSON String a Object
	then(setOfJsonObjects => saveCluster(setOfJsonObjects)). //obtengo una lista de nodos
	done(drawer.draw()); //Actualizo los nodos en memoria
}


requestInfo();
setInterval(requestInfo, 5000);

//En JavaScript, al llamar una función func con paréntesis (I.E func()) se ejecuta y devuleve
//el valor que retorna la función. En cambio, si se pasa solamente el nombre de la variable (I.E func)
//esa variable si contiene el valor de una función. Para una explicación más detallada: 
//https://stackoverflow.com/questions/8779845/javascript-setinterval-not-working

