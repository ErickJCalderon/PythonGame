"""Clase nodo para saber el movimiento en base al algoritmo de Dijkstra y DFS"""


class Nodo:
    parent = None
    weight = None
    direction = 1

    def __init__(self, px, py, reach, base_weight, value):
        self.x = px
        self.y = py
        self.reach = reach
        self.base_weight = base_weight
        self.value = value
