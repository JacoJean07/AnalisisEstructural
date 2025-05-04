# core/estructura.py
class Nodo:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y


class Elemento:
    def __init__(self, id, nodo_inicio, nodo_fin):
        self.id = id
        self.nodo_inicio = nodo_inicio
        self.nodo_fin = nodo_fin