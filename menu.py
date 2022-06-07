import pygame
import pygame_menu

import juego
from algoritmo import Algoritmo

COLOR_BACKGROUND = (153, 255, 153)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (229, 130, 31)
MENU_TITLE_COLOR = (144, 198, 227)

pygame.display.init()
INFO = pygame.display.Info()
TILE_SIZE = int(INFO.current_h * 0.035)
WINDOW_SIZE = (13 * TILE_SIZE, 13 * TILE_SIZE)

clock = None
player_alg = Algoritmo.PLAYER
bot1_alg = Algoritmo.DIJKSTRA
bot2_alg = Algoritmo.DFS
bot3_alg = Algoritmo.DIJKSTRA
mostrar_camino = True
surface = pygame.display.set_mode(WINDOW_SIZE)


def change_path(value, c):
    global mostrar_camino
    mostrar_camino = c


def change_player(value, c):
    global player_alg
    player_alg = c


def change_enemy1(value, c):
    global bot1_alg
    bot1_alg = c


def change_enemy2(value, c):
    global bot2_alg
    bot2_alg = c


def change_enemy3(value, c):
    global bot3_alg
    bot3_alg = c


def run_game():
    juego.game_init(mostrar_camino, player_alg, bot1_alg, bot2_alg, bot3_alg, TILE_SIZE)


def main_background():
    global surface
    surface.fill(COLOR_BACKGROUND)


"""Import del menu para que se ejecute"""


def menu_loop():
    pygame.init()

    pygame.display.set_caption('Bomberman')
    clock = pygame.time.Clock()

    menu_theme = pygame_menu.themes.Theme(selection_color=COLOR_WHITE,
                                          widget_font=pygame_menu.font.FONT_BEBAS,
                                          title_font_size=int(TILE_SIZE * 0.8),
                                          title_font_color=COLOR_BLACK,
                                          title_font=pygame_menu.font.FONT_BEBAS,
                                          widget_font_color=COLOR_BLACK,
                                          widget_font_size=int(TILE_SIZE * 0.7),
                                          background_color=MENU_BACKGROUND_COLOR,
                                          title_background_color=MENU_TITLE_COLOR,
                                          )

    play_menu = pygame_menu.Menu(
        theme=menu_theme,
        height=int(WINDOW_SIZE[1] * 0.7),
        width=int(WINDOW_SIZE[0] * 0.7),
        title='Menu  de  Juego'
    )

    play_options = pygame_menu.Menu(theme=menu_theme,
                                    height=int(WINDOW_SIZE[1] * 0.7),
                                    width=int(WINDOW_SIZE[0] * 0.7),
                                    title='Opciones'
                                    )
    play_options.add.selector("Personaje 1", [("Jugador", Algoritmo.PLAYER), ("DFS", Algoritmo.DFS),
                                              ("DIJKSTRA", Algoritmo.DIJKSTRA), ("None", Algoritmo.NONE)],
                              onchange=change_player)
    play_options.add.selector("Personaje 2", [("DIJKSTRA", Algoritmo.DIJKSTRA), ("DFS", Algoritmo.DFS),
                                              ("None", Algoritmo.NONE)], onchange=change_enemy1)
    play_options.add.selector("Personaje 3", [("DIJKSTRA", Algoritmo.DIJKSTRA), ("DFS", Algoritmo.DFS),
                                              ("None", Algoritmo.NONE)], onchange=change_enemy2, default=1)
    play_options.add.selector("Personaje 4", [("DIJKSTRA", Algoritmo.DIJKSTRA), ("DFS", Algoritmo.DFS),
                                              ("None", Algoritmo.NONE)], onchange=change_enemy3)
    play_options.add.selector("Mostrar camino", [("Yes", True), ("No", False)], onchange=change_path)

    play_options.add.button('Atras', pygame_menu.events.BACK)
    play_menu.add.button('Empezar',
                         run_game)

    play_menu.add.button('Opciones', play_options)
    play_menu.add.button('Volver al menu principal', pygame_menu.events.BACK)

    about_menu_theme = pygame_menu.themes.Theme(
        selection_color=COLOR_WHITE,
        widget_font=pygame_menu.font.FONT_BEBAS,
        title_font_size=TILE_SIZE,
        title_font_color=COLOR_BLACK,
        title_font=pygame_menu.font.FONT_BEBAS,
        widget_font_color=COLOR_BLACK,
        widget_font_size=int(TILE_SIZE * 0.4),
        background_color=MENU_BACKGROUND_COLOR,
        title_background_color=MENU_TITLE_COLOR,
    )

    about_menu = pygame_menu.Menu(theme=about_menu_theme,
                                  height=int(WINDOW_SIZE[1] * 0.7),
                                  width=int(WINDOW_SIZE[0] * 0.7),
                                  title='About'
                                  )
    about_menu.add.label("Controles del Jugador: ")
    about_menu.add.label("Moverse: Flechas")
    about_menu.add.label("Poner bomba:Space bar")
    about_menu.add.label("Autor: Erick Calderon")

    main_menu = pygame_menu.Menu(
        theme=menu_theme,
        height=int(WINDOW_SIZE[1] * 0.6),
        width=int(WINDOW_SIZE[0] * 0.6),
        title='Menu  Principal'
    )

    main_menu.add.button('Jugar', play_menu)
    main_menu.add.button('Acerca de', about_menu)
    main_menu.add.button('Salir', pygame_menu.events.EXIT)
    while True:

        clock.tick(FPS)

        main_background()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        main_menu.mainloop(surface, main_background, disable_loop=False, fps_limit=0)
        main_menu.actualizar(events)
        main_menu.empate(surface)

        pygame.display.flip()


menu_loop()
