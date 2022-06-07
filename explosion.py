class Explosion:

    bomber = None

    def __init__(self, x, y, r):
        self.sourceX = x
        self.sourceY = y
        self.range = r
        self.time = 300
        self.frame = 0
        self.sectors = []

    """Explosion de la bomba"""
    def explode(self, map, bombs, b):

        self.bomber = b.bomber
        self.sectors.extend(b.sectors)
        bombs.remove(b)
        self.bomba_cadena(bombs, map)

    """La llama de la bomba al explotar"""
    def bomba_cadena(self, bombs, map):

        for s in self.sectors:
            for x in bombs:
                if x.posX == s[0] and x.posY == s[1]:

                    map[x.posX][x.posY] = 0
                    x.bomber.bomb_limit += 1
                    self.explode(map, bombs, x)

    """Resets de las casillas o sectores para el control de las estructuras rotas"""
    def limpiar_sectors(self, mapa):

        for i in self.sectors:
            mapa[i[0]][i[1]] = 0

    def update(self, dt):

        self.time = self.time - dt

        if self.time < 100:
            self.frame = 2
        elif self.time < 200:
            self.frame = 1
