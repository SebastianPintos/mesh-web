from mapView.models import Node


class LightChangesAnalizer:
    # Al comenzar, trae los cambio de la base de datos y los gaurda en memoria
    def __init__(self):
        self.BASE_MINIMUM_AMPERAGE = 0.8

        self.TURNED_ON_LIGHT = 'VERDE'
        self.TURNED_OFF_LIGHT = 'AMARILLO'
        self.POWEROFF_NODE = 'ROJO'

        self.nodes = Node.objects.all()

    def __save_changes(self, n_ip, node_status):
        # al detectar un cambio los guarda en la base de datos
        Node.objects.filter(node_ip=n_ip).update(node_states=node_status)

    # comparo los nodos en memoria, si detecto un cambio, aviso el cambio (Y despues que hago con los cambios? (los
    # guardo a penas lo reconozco?))
    def __compare_node_states(self, light_amperage, n_ip):
        actual_state = self.nodes.get(node_ip=n_ip).node_states
        # Si el estado difiere del actual_state (debería haber un tiempo) cambiar
        if actual_state == self.TURNED_ON_LIGHT and not self.__is_turned_on(light_amperage):
            # Avisar de (pasar a amarillo)
            self.__save_changes(n_ip, self.TURNED_OFF_LIGHT)
            return "AMARILLO"
        if actual_state == self.TURNED_OFF_LIGHT and self.__is_turned_on(light_amperage):
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
        amperage = udp_package.values['current']

        print("El amperaje es: ", amperage)
        print("Lo que devuelve el metodo es: ", self.__compare_node_states(amperage, ip))
