import pygame
import sys
import random
import time
from jugador import Jugador
from explosion import Explosion
from bot import Bot
from algoritmo import Algoritmo

TITLE_WIDTH = 40
TITLE_HEIGHT = 40

WINDOW_WIDTH = 13 * TITLE_WIDTH
WINDOW_HEIGHT = 13 * TITLE_HEIGHT

BACKGROUND = (107, 142, 35)

s = None
mostrar_camino = True

clock = None

jugador = None
bot_list = []
bot_blocks = []
bombas = []
explosiones = []

tablero = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

img_suelo = None
img_bloque = None
img_caja = None
img_bomba = None
img_bomba2 = None
img_bomba3 = None
img_explosion = None
img_explosion2 = None
img_explosion3 = None

imagenes_tablero = []
imagenes_bomba = []
imagenes_explosion = []

pygame.font.init()
font = pygame.font.SysFont('Arial', 30)
TEXT_LOSE = font.render('GAME OVER', False, (0, 0, 0))
TEXT_WIN = font.render('GANASTE', False, (0, 0, 0))

"""Funcion que inicia el juego"""


def game_init(path, jugador_alg, bot1_alg, bot2_alg, bot3_alg, scale):
    global TITLE_WIDTH
    global TITLE_HEIGHT
    TITLE_WIDTH = scale
    TITLE_HEIGHT = scale

    global font
    font = pygame.font.SysFont('Arial', scale)

    global mostrar_camino
    mostrar_camino = path

    global s
    s = pygame.display.set_mode((13 * TITLE_WIDTH, 13 * TITLE_HEIGHT))
    pygame.display.set_caption('Bomberman')

    global clock
    clock = pygame.time.Clock()

    global bot_list
    global bot_blocks
    global jugador

    bot_list = []
    bot_blocks = []
    global explosiones
    global bombas
    bombas.clear()
    explosiones.clear()

    jugador = Jugador()

    if bot1_alg is not Algoritmo.NONE:
        bot1 = Bot(11, 11, bot1_alg)
        bot1.cargar_animaciones('1', scale)
        bot_list.append(bot1)
        bot_blocks.append(bot1)

    if bot2_alg is not Algoritmo.NONE:
        bot2 = Bot(1, 11, bot2_alg)
        bot2.cargar_animaciones('2', scale)
        bot_list.append(bot2)
        bot_blocks.append(bot2)

    if bot3_alg is not Algoritmo.NONE:
        bot3 = Bot(11, 1, bot3_alg)
        bot3.cargar_animaciones('3', scale)
        bot_list.append(bot3)
        bot_blocks.append(bot3)

    if jugador_alg is Algoritmo.PLAYER:
        jugador.cargar_animaciones(scale)
        bot_blocks.append(jugador)

    elif jugador_alg is not Algoritmo.NONE:
        bot0 = Bot(1, 1, jugador_alg)
        bot0.cargar_animaciones('', scale)
        bot_list.append(bot0)
        bot_blocks.append(bot0)
        jugador.life = False
    else:
        jugador.life = False

    global img_suelo
    img_suelo = pygame.image.load('images/terrain/grass.png')
    img_suelo = pygame.transform.scale(img_suelo, (TITLE_WIDTH, TITLE_HEIGHT))
    global img_bloque
    img_bloque = pygame.image.load('images/terrain/block.png')
    img_bloque = pygame.transform.scale(img_bloque, (TITLE_WIDTH, TITLE_HEIGHT))
    global img_caja
    img_caja = pygame.image.load('images/terrain/box.png')
    img_caja = pygame.transform.scale(img_caja, (TITLE_WIDTH, TITLE_HEIGHT))
    global img_bomba
    img_bomba = pygame.image.load('images/bomb/1.png')
    img_bomba = pygame.transform.scale(img_bomba, (TITLE_WIDTH, TITLE_HEIGHT))
    global img_bomba2
    img_bomba2 = pygame.image.load('images/bomb/2.png')
    img_bomba2 = pygame.transform.scale(img_bomba2, (TITLE_WIDTH, TITLE_HEIGHT))
    global img_bomba3
    img_bomba3 = pygame.image.load('images/bomb/3.png')
    img_bomba3 = pygame.transform.scale(img_bomba3, (TITLE_WIDTH, TITLE_HEIGHT))
    global img_explosion
    img_explosion = pygame.image.load('images/explosion/1.png')
    img_explosion = pygame.transform.scale(img_explosion, (TITLE_WIDTH, TITLE_HEIGHT))
    global img_explosion2
    img_explosion2 = pygame.image.load('images/explosion/2.png')
    img_explosion2 = pygame.transform.scale(img_explosion2, (TITLE_WIDTH, TITLE_HEIGHT))
    global img_explosion3
    img_explosion3 = pygame.image.load('images/explosion/3.png')
    img_explosion3 = pygame.transform.scale(img_explosion3, (TITLE_WIDTH, TITLE_HEIGHT))
    global imagenes_tablero
    imagenes_tablero = [img_suelo, img_bloque, img_caja, img_suelo]
    global imagenes_bomba
    imagenes_bomba = [img_bomba, img_bomba2, img_bomba3]
    global imagenes_explosion
    imagenes_explosion = [img_explosion, img_explosion2, img_explosion3]

    main()


"""Cuando exite un empate"""


def empate():
    s.fill(BACKGROUND)
    for i in range(len(tablero)):
        for j in range(len(tablero[i])):
            s.blit(imagenes_tablero[tablero[i][j]], (i * TITLE_WIDTH, j * TITLE_HEIGHT, TITLE_HEIGHT, TITLE_WIDTH))

    for x in bombas:
        s.blit(imagenes_bomba[x.frame], (x.posX * TITLE_WIDTH, x.posY * TITLE_HEIGHT, TITLE_HEIGHT, TITLE_WIDTH))

    for y in explosiones:
        for x in y.sectors:
            s.blit(imagenes_explosion[y.frame], (x[0] * TITLE_WIDTH, x[1] * TITLE_HEIGHT, TITLE_HEIGHT, TITLE_WIDTH))
    if jugador.life:
        s.blit(jugador.animation[jugador.direction][jugador.frame],
               (jugador.posX * (TITLE_WIDTH / 4), jugador.posY * (TITLE_HEIGHT / 4), TITLE_WIDTH, TITLE_HEIGHT))
    for bot in bot_list:
        if bot.life:
            s.blit(bot.animation[bot.direction][bot.frame],
                   (bot.posX * (TITLE_WIDTH / 4), bot.posY * (TITLE_HEIGHT / 4), TITLE_WIDTH, TITLE_HEIGHT))
            if mostrar_camino:
                if bot.algorithm == Algoritmo.DFS:
                    for buscar in bot.path:
                        pygame.draw.rect(s, (255, 0, 0, 240),
                                         [buscar[0] * TITLE_WIDTH, buscar[1] * TITLE_HEIGHT, TITLE_WIDTH, TITLE_WIDTH],
                                         1)
                else:
                    for buscar in bot.path:
                        pygame.draw.rect(s, (255, 0, 255, 240),
                                         [buscar[0] * TITLE_WIDTH, buscar[1] * TITLE_HEIGHT, TITLE_WIDTH, TITLE_WIDTH],
                                         1)

    pygame.display.update()


"""Generador mapas random"""


def generar_mapa():
    for i in range(1, len(tablero) - 1):
        for j in range(1, len(tablero[i]) - 1):
            if tablero[i][j] != 0:
                continue
            elif (i < 3 or i > len(tablero) - 4) and (j < 3 or j > len(tablero[i]) - 4):
                continue
            if random.randint(0, 9) < 7:
                tablero[i][j] = 2

    return


"""Funcion main"""


def main():
    generar_mapa()
    while jugador.life:
        dt = clock.tick(15)
        for en in bot_list:
            en.realizar_movimiento(tablero, bombas, explosiones, bot_blocks)
        keys = pygame.key.get_pressed()
        temp = jugador.direction
        movement = False
        if keys[pygame.K_DOWN]:
            temp = 0
            jugador.move(0, 1, tablero, bot_blocks)
            movement = True
        elif keys[pygame.K_RIGHT]:
            temp = 1
            jugador.move(1, 0, tablero, bot_blocks)
            movement = True
        elif keys[pygame.K_UP]:
            temp = 2
            jugador.move(0, -1, tablero, bot_blocks)
            movement = True
        elif keys[pygame.K_LEFT]:
            temp = 3
            jugador.move(-1, 0, tablero, bot_blocks)
            movement = True

        if temp != jugador.direction:
            jugador.frame = 0
            jugador.direction = temp
        if movement:
            if jugador.frame == 2:
                jugador.frame = 0
            else:
                jugador.frame += 1

        empate()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit(0)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if jugador.bomb_limit == 0:
                        continue
                    temp_bomba = jugador.plantar_bomba(tablero)
                    bombas.append(temp_bomba)
                    tablero[temp_bomba.posX][temp_bomba.posY] = 3
                    jugador.bomb_limit -= 1

        actualizar_bombas(dt)
    game_over()


"""Checker de las bombas"""


def actualizar_bombas(dt):
    for b in bombas:
        b.update(dt)
        if b.time < 1:
            b.bomber.bomb_limit += 1
            tablero[b.posX][b.posY] = 0
            exp_temp = Explosion(b.posX, b.posY, b.range)
            exp_temp.explode(tablero, bombas, b)
            exp_temp.limpiar_sectors(tablero)
            explosiones.append(exp_temp)
    if jugador not in bot_list:
        jugador.checkear_muerte(explosiones)
    for en in bot_list:
        en.checkear_muerte(explosiones)
    for e in explosiones:
        e.update(dt)
        if e.time < 1:
            explosiones.remove(e)


"""Funcion para terminar el juego"""


def game_over():
    while True:
        dt = clock.tick(15)
        actualizar_bombas(dt)
        count = 0
        ganador = ""
        for bot in bot_list:
            bot.realizar_movimiento(tablero, bombas, explosiones, bot_blocks)
            if bot.life:
                count += 1
                ganador = bot.algorithm.name
        if count == 1:
            empate()
            textsurface = font.render(ganador + " gano", False, (255, 255, 255))
            font_w = textsurface.get_width()
            font_h = textsurface.get_height()
            s.blit(textsurface, (s.get_width() // 2 - font_w // 2, s.get_height() // 2 - font_h // 2))
            pygame.display.update()
            time.sleep(2)
            break
        if count == 0:
            empate()
            textsurface = font.render("Empate", False, (255, 255, 255))
            font_w = textsurface.get_width()
            font_h = textsurface.get_height()
            s.blit(textsurface, (s.get_width() // 2 - font_w // 2, s.get_height() // 2 - font_h // 2))
            pygame.display.update()
            time.sleep(2)
            break
        empate()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit(0)
    explosiones.clear()
    bot_list.clear()
    bot_blocks.clear()
