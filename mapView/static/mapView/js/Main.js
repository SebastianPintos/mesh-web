var map = new Map("meshMap");
map.init();

var node1 = new Node([-34.542362, -58.712332], "192.168.1.1", "GRIS");

var cluster = getCluster();

cluster.map(node => map.addNode(node));
