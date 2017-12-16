var map = new Map("meshMap");
map.init();

var cluster = getCluster();

cluster.map(node => map.addNode(node));
