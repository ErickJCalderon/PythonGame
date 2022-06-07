class Bomba:
    frame = 0

    def __init__(self, r, x, y, mapa, bomber):
        self.range = r
        self.posX = x
        self.posY = y
        self.time = 3000
        self.bomber = bomber
        self.sectors = []
        self.get_range(mapa)

    def update(self, dt):

        self.time = self.time - dt

        if self.time < 1000:
            self.frame = 2
        elif self.time < 2000:
            self.frame = 1

    """Llamada al rango de la bomba"""
    def get_range(self, mapa):

        self.sectors.append([self.posX, self.posY])

        for x in range(1, self.range):
            if mapa[self.posX + x][self.posY] == 1:
                break
            elif mapa[self.posX + x][self.posY] == 0 or mapa[self.posX - x][self.posY] == 3:
                self.sectors.append([self.posX+x, self.posY])
            elif mapa[self.posX + x][self.posY] == 2:
                self.sectors.append([self.posX+x, self.posY])
                break
        for x in range(1, self.range):
            if mapa[self.posX - x][self.posY] == 1:
                break
            elif mapa[self.posX - x][self.posY] == 0 or mapa[self.posX - x][self.posY] == 3:
                self.sectors.append([self.posX-x, self.posY])
            elif mapa[self.posX - x][self.posY] == 2:
                self.sectors.append([self.posX-x, self.posY])
                break
        for x in range(1, self.range):
            if mapa[self.posX][self.posY + x] == 1:
                break
            elif mapa[self.posX][self.posY + x] == 0 or mapa[self.posX][self.posY + x] == 3:
                self.sectors.append([self.posX, self.posY+x])
            elif mapa[self.posX][self.posY + x] == 2:
                self.sectors.append([self.posX, self.posY+x])
                break
        for x in range(1, self.range):
            if mapa[self.posX][self.posY - x] == 1:
                break
            elif mapa[self.posX][self.posY - x] == 0 or mapa[self.posX][self.posY - x] == 3:
                self.sectors.append([self.posX, self.posY-x])
            elif mapa[self.posX][self.posY - x] == 2:
                self.sectors.append([self.posX, self.posY - x])
                break
