from mapView.models import Node

class LightChangesAnalizer:
    #Al comenzar, trae los cambio de la base de datos y los gaurda en memoria
    BASE_MINIMUM_AMPERAGE = 0.1

    TURNED_ON_LIGHT = 'VERDE'
    TURNED_OFF_LIGHT= 'AMARILLO'
    POWEROFF_NODE = 'ROJO'

    def __init__(self):
        #Declaor un diccionar,
        self.nodes = Node.objects.all();

    def __save_changes(self, n_ip, node_status):
        #al detectar un cambio los guarda en la base de datos
        Node.objects.filter(node_ip = n_ip).update(node_states = node_status)

    #comparo los nodos en memoria, si detecto un cambio, aviso el cambio (Y despues que hago con los cambios? (los guardo a penas lo reconozco?))
    def __compare_node_states(self, light_amperage, n_ip):
        actual_state = self.nodes.get(node_ip = n_ip).node_states
        #Si el estado difiere del actual_state (debería haber un tiempo) cambiar
        if actual_state == TURNED_ON_LIGHT and not __isTurnedOn(light_amperage):
            #Avisar de (pasar a amarillo)
            return TURNED_OFF_LIGHT

        if actual_state == TURNED_OFF_LIGHT and __isTurnedOn(light_amperage):
            #Avisar de (pasar a verde)
            return TURNED_ON_LIGHT

        return actual_state # pasar un estado para que no se escriba en memoria



    def __isTurnedOn(light_state):
        #Mide si los datos corresponden a una luz prendida o a una luz apagada
        return light_state >= BASE_MINIMUM_AMPERAGE
