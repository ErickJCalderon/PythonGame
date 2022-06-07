import pygame
import random
from bomba import Bomba
from nodo import Nodo
from algoritmo import Algoritmo


class Bot:
    dire = [[1, 0, 1], [0, 1, 0], [-1, 0, 3], [0, -1, 2]]

    def __init__(self, x, y, alg):
        self.life = True
        self.path = []
        self.movement_path = []
        self.posX = x * 4
        self.posY = y * 4
        self.direction = 0
        self.frame = 0
        self.animation = []
        self.range = 3
        self.bomb_limit = 1
        self.plant = False
        self.algorithm = alg

    def movimiento(self, mapa, bombas, explosiones, bot):

        if self.direction == 0:
            self.posY += 1
        elif self.direction == 1:
            self.posX += 1
        elif self.direction == 2:
            self.posY -= 1
        elif self.direction == 3:
            self.posX -= 1

        if self.posX % 4 == 0 and self.posY % 4 == 0:
            self.movement_path.pop(0)
            self.path.pop(0)
            if len(self.path) > 1:
                casilla = self.crear_casilla(mapa, bombas, explosiones, bot)
                siguiente = self.path[1]
                if casilla[siguiente[0]][siguiente[1]] > 1:
                    self.movement_path.clear()
                    self.path.clear()

        if self.frame == 2:
            self.frame = 0
        else:
            self.frame += 1

    def realizar_moveimiento(self, mapa, bombas, explosiones, bot):

        if not self.life:
            return
        if len(self.movement_path) == 0:
            if self.plant:
                bombas.append(self.plantar_bomba(mapa))
                self.plant = False
                mapa[int(self.posX / 4)][int(self.posY / 4)] = 3
            if self.algorithm is Algoritmo.DFS:
                self.dfs(self.crear_casilla(mapa, bombas, explosiones, bot))
            else:
                self.dijkstra(self.crear_casilla_dijkstra(mapa, bombas, explosiones, bot))

        else:
            self.direction = self.movement_path[0]
            self.movimiento(mapa, bombas, explosiones, bot)

    def plantar_bomba(self, mapa):
        b = Bomba(self.range, round(self.posX / 4), round(self.posY / 4), mapa, self)
        self.bomb_limit -= 1
        return b

    def checkear_muerte(self, exp):

        for e in exp:
            for s in e.sectors:
                if int(self.posX / 4) == s[0] and int(self.posY / 4) == s[1]:
                    if e.bomber == self:
                        print(str(self.algorithm.value) + " SUICIDE")
                    self.life = False
                    return

    def dfs(self, casilla):

        nuevo_path = [[int(self.posX / 4), int(self.posY / 4)]]
        depth = 0
        if self.bomb_limit == 0:
            self.dfs_rec(casilla, 0, nuevo_path, depth)
        else:
            self.dfs_rec(casilla, 2, nuevo_path, depth)

        self.path = nuevo_path

    def dfs_rec(self, casilla, end, path, depth):

        last = path[-1]
        if depth > 200:
            return
        if casilla[last[0]][last[1]] == 0 and end == 0:
            return
        elif end == 2:
            if casilla[last[0] + 1][last[1]] == end or casilla[last[0] - 1][last[1]] == end \
                    or casilla[last[0]][last[1] + 1] == end \
                    or casilla[last[0]][last[1] - 1] == end:
                if len(path) == 1 and end == 2:
                    self.plant = True
                return

        casilla[last[0]][last[1]] = 9

        random.shuffle(self.dire)

        # safe
        if casilla[last[0] + self.dire[0][0]][last[1] + self.dire[0][1]] == 0:
            path.append([last[0] + self.dire[0][0], last[1] + self.dire[0][1]])
            self.movement_path.append(self.dire[0][2])
        elif casilla[last[0] + self.dire[1][0]][last[1] + self.dire[1][1]] == 0:
            path.append([last[0] + self.dire[1][0], last[1] + self.dire[1][1]])
            self.movement_path.append(self.dire[1][2])
        elif casilla[last[0] + self.dire[2][0]][last[1] + self.dire[2][1]] == 0:
            path.append([last[0] + self.dire[2][0], last[1] + self.dire[2][1]])
            self.movement_path.append(self.dire[2][2])
        elif casilla[last[0] + self.dire[3][0]][last[1] + self.dire[3][1]] == 0:
            path.append([last[0] + self.dire[3][0], last[1] + self.dire[3][1]])
            self.movement_path.append(self.dire[3][2])

        # unsafe
        elif casilla[last[0] + self.dire[0][0]][last[1] + self.dire[0][1]] == 1:
            path.append([last[0] + self.dire[0][0], last[1] + self.dire[0][1]])
            self.movement_path.append(self.dire[0][2])
        elif casilla[last[0] + self.dire[1][0]][last[1] + self.dire[1][1]] == 1:
            path.append([last[0] + self.dire[1][0], last[1] + self.dire[1][1]])
            self.movement_path.append(self.dire[1][2])
        elif casilla[last[0] + self.dire[2][0]][last[1] + self.dire[2][1]] == 1:
            path.append([last[0] + self.dire[2][0], last[1] + self.dire[2][1]])
            self.movement_path.append(self.dire[2][2])
        elif casilla[last[0] + self.dire[3][0]][last[1] + self.dire[3][1]] == 1:
            path.append([last[0] + self.dire[3][0], last[1] + self.dire[3][1]])
            self.movement_path.append(self.dire[3][2])
        else:
            if len(self.movement_path) > 0:
                path.pop(0)
                self.movement_path.pop(0)
        depth += 1
        self.dfs_rec(casilla, end, path, depth)

    def dijkstra(self, casilla):

        end = 1
        if self.bomb_limit == 0:
            end = 0

        visitado = []
        abrir_lista = []
        actual = casilla[int(self.posX / 4)][int(self.posY / 4)]
        actual.weight = actual.base_weight
        nuevo_path = []
        while True:
            visitado.append(actual)
            random.shuffle(self.dire)
            if (actual.value == end and end == 0) or \
                    (end == 1 and (
                            casilla[actual.x + 1][actual.y].value == 1 or casilla[actual.x - 1][actual.y].value == 1 or
                            casilla[actual.x][actual.y + 1].value == 1 or casilla[actual.x][actual.y - 1].value == 1)):
                nuevo_path.append([actual.x, actual.y])
                while True:
                    if actual.parent is None:
                        break
                    actual = actual.parent
                    nuevo_path.append([actual.x, actual.y])
                nuevo_path.reverse()
                for xd in range(len(nuevo_path)):
                    if nuevo_path[xd] is not nuevo_path[-1]:
                        if nuevo_path[xd][0] - nuevo_path[xd + 1][0] == -1:
                            self.movement_path.append(1)
                        elif nuevo_path[xd][0] - nuevo_path[xd + 1][0] == 1:
                            self.movement_path.append(3)
                        elif nuevo_path[xd][1] - nuevo_path[xd + 1][1] == -1:
                            self.movement_path.append(0)
                        elif nuevo_path[xd][1] - nuevo_path[xd + 1][1] == 1:
                            self.movement_path.append(2)
                if len(nuevo_path) == 1 and end == 1:
                    self.plant = True
                self.path = nuevo_path
                return

            for i in range(len(self.dire)):
                if actual.x + self.dire[i][0] < len(casilla) and actual.y + self.dire[i][1] < len(casilla):
                    if casilla[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].reach and casilla[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]] not in visitado:
                        if casilla[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]] in abrir_lista:
                            if casilla[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].weight > casilla[actual.x][actual.y].weight  + casilla[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].base_weight:
                                casilla[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].parent = actual
                                casilla[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].weight = actual.weight + casilla[ actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].base_weight
                                casilla[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].direction = self.dire[i][2]

                        else:
                            casilla[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].parent = actual
                            casilla[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].weight = actual.weight + casilla[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].base_weight
                            casilla[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]].direction = self.dire[i][2]
                            abrir_lista.append(casilla[actual.x + self.dire[i][0]][actual.y + self.dire[i][1]])

            if len(abrir_lista) == 0:
                self.path = [[int(self.posX / 4), int(self.posY / 4)]]
                return

            siguiente_nodo = abrir_lista[0]
            for n in abrir_lista:
                if n.weight < siguiente_nodo.weight:
                    siguiente_nodo = n
            abrir_lista.remove(siguiente_nodo)
            actual = siguiente_nodo

    def crear_casilla(self, mapa, bombas, explosiones, bots):
        casilla = [[0] * len(mapa) for r in range(len(mapa))]

        # 0 - safe
        # 1 - unsafe
        # 2 - destryable
        # 3 - unreachable

        for b in bombas:
            b.get_range(mapa)
            for x in b.sectors:
                casilla[x[0]][x[1]] = 1
            casilla[b.posX][b.posY] = 3

        for e in explosiones:
            for s in e.sectors:
                casilla[s[0]][s[1]] = 3

        for i in range(len(mapa)):
            for j in range(len(mapa[i])):
                if mapa[i][j] == 1:
                    casilla[i][j] = 3
                elif mapa[i][j] == 2:
                    casilla[i][j] = 2

        for x in bots:
            if x == self:
                continue
            elif not x.life:
                continue
            else:
                casilla[int(x.posX / 4)][int(x.posY / 4)] = 2

        return casilla

    def crear_casilla_dijkstra(self, mapa, bombas, explosiones, bots):
        casilla = [[None] * len(mapa) for r in range(len(mapa))]

        # 0 - a salvo
        # 1 - destruible
        # 2 - inalcanzable
        # 3 - inseguro
        for i in range(len(mapa)):
            for j in range(len(mapa)):
                if mapa[i][j] == 0:
                    casilla[i][j] = Nodo(i, j, True, 1, 0)
                elif mapa[i][j] == 2:
                    casilla[i][j] = Nodo(i, j, False, 999, 1)
                elif mapa[i][j] == 1:
                    casilla[i][j] = Nodo(i, j, False, 999, 2)
                elif mapa[i][j] == 3:
                    casilla[i][j] = Nodo(i, j, False, 999, 2)

        for b in bombas:
            b.get_range(mapa)
            for x in b.sectors:
                casilla[x[0]][x[1]].weight = 5
                casilla[x[0]][x[1]].value = 3
            casilla[b.posX][b.posY].reach = False

        for e in explosiones:
            for s in e.sectors:
                casilla[s[0]][s[1]].reach = False

        for x in bots:
            if x == self:
                continue
            elif not x.life:
                continue
            else:
                casilla[int(x.posX / 4)][int(x.posY / 4)].reach = False
                casilla[int(x.posX / 4)][int(x.posY / 4)].value = 1
        return casilla

    def cargar_animaciones(self, en, scale):
        front = []
        back = []
        left = []
        right = []
        resize_width = scale
        resize_height = scale

        image_path = 'images/enemy/e'
        if en == '':
            image_path = 'images/hero/p'

        f1 = pygame.image.load(image_path + en + 'f0.png')
        f2 = pygame.image.load(image_path + en + 'f1.png')
        f3 = pygame.image.load(image_path + en + 'f2.png')

        f1 = pygame.transform.scale(f1, (resize_width, resize_height))
        f2 = pygame.transform.scale(f2, (resize_width, resize_height))
        f3 = pygame.transform.scale(f3, (resize_width, resize_height))

        front.append(f1)
        front.append(f2)
        front.append(f3)

        r1 = pygame.image.load(image_path + en + 'r0.png')
        r2 = pygame.image.load(image_path + en + 'r1.png')
        r3 = pygame.image.load(image_path + en + 'r2.png')

        r1 = pygame.transform.scale(r1, (resize_width, resize_height))
        r2 = pygame.transform.scale(r2, (resize_width, resize_height))
        r3 = pygame.transform.scale(r3, (resize_width, resize_height))

        right.append(r1)
        right.append(r2)
        right.append(r3)

        b1 = pygame.image.load(image_path + en + 'b0.png')
        b2 = pygame.image.load(image_path + en + 'b1.png')
        b3 = pygame.image.load(image_path + en + 'b2.png')

        b1 = pygame.transform.scale(b1, (resize_width, resize_height))
        b2 = pygame.transform.scale(b2, (resize_width, resize_height))
        b3 = pygame.transform.scale(b3, (resize_width, resize_height))

        back.append(b1)
        back.append(b2)
        back.append(b3)

        l1 = pygame.image.load(image_path + en + 'l0.png')
        l2 = pygame.image.load(image_path + en + 'l1.png')
        l3 = pygame.image.load(image_path + en + 'l2.png')

        l1 = pygame.transform.scale(l1, (resize_width, resize_height))
        l2 = pygame.transform.scale(l2, (resize_width, resize_height))
        l3 = pygame.transform.scale(l3, (resize_width, resize_height))

        left.append(l1)
        left.append(l2)
        left.append(l3)

        self.animation.append(front)
        self.animation.append(right)
        self.animation.append(back)
        self.animation.append(left)
