from mapView.models import Node, NodeLogCurrentRecords
from datetime import datetime, timedelta
import pytz, threading, time

class LightChangesAnalizer:
    # Al comenzar, trae los cambio de la base de datos y los gaurda en memoria
    def __init__(self):
        self.BASE_MINIMUM_AMPERAGE = 0.8

        self.TURNED_ON_LIGHT = 'VERDE'
        self.TURNED_OFF_LIGHT = 'AMARILLO'
        self.POWEROFF_NODE = 'ROJO'

        self.nodes = Node.objects.all()

        d = threading.Thread(target=self.__analyze_living_arduino, name='listener')
        d.setDaemon(True)
        d.start()

    def __save_changes(self, n_ip, node_status):
        # al detectar un cambio los guarda en la base de datos
        Node.objects.filter(node_ip=n_ip).update(node_states=node_status)

    # comparo los nodos en memoria, si detecto un cambio, aviso el cambio (Y despues que hago con los cambios? (los
    # guardo a penas lo reconozco?))
    # actual_state == self.TURNED_OFF_LIGHT and
    # actual_state == self.TURNED_ON_LIGHT and
    def __compare_node_states(self, light_amperage, n_ip):
        actual_state = self.nodes.get(node_ip=n_ip).node_states
        # Si el estado difiere del actual_state (debería haber un tiempo) cambiar
        if  not self.__is_turned_on(light_amperage):
            # Avisar de (pasar a amarillo)
            self.__save_changes(n_ip, self.TURNED_OFF_LIGHT)
            return "AMARILLO"
        if  self.__is_turned_on(light_amperage):
            # Avisar de (pasar a verde)
            self.__save_changes(n_ip, self.TURNED_ON_LIGHT)
            return "VERDE"
        # return actual_state # pasar un estado para que no se escriba en memoria

    def __is_turned_on(self, light_state):
        # Mide si los datos corresponden a una luz prendida o a una luz apagada
        return light_state >= self.BASE_MINIMUM_AMPERAGE

    def analyze_data(self, udp_package):
        if udp_package.type != 0:
            return

        ip = udp_package.ip
        amperage = udp_package.values

        print("El amperaje es: ", amperage)
        print("Lo que devuelve el metodo es: ", self.__compare_node_states(amperage, ip))

    def __analyze_living_arduino(self):
        while 1:
            for node in self.nodes:
                if(self.__has_expired(node)):
                    if(node.node_states != self.POWEROFF_NODE):
                        self.__save_changes(node.node_ip, "VIOLETA")
            time.sleep(60)

    def __has_expired(self, node):
        expected_time = timedelta(minutes=1)

        utc=pytz.UTC

        actual_date = datetime.now()
        node_date = NodeLogCurrentRecords.objects.filter(record_node = node).last().record_date


        actual_date = actual_date.replace(tzinfo=utc)
        node_date = node_date.replace(tzinfo=utc)

        difference = actual_date - node_date
        print("La difrencia con el último registro de ", node.node_ip, " es: ", difference)

        return difference > expected_time
