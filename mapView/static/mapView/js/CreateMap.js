leafletMap = L.map('meshMap')
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(leafletMap);

leafletMap.setView([-34.542960, -58.711922], 18);

var drawer = new Drawer(leafletMap);
var nodes = [];
var markers = [];
