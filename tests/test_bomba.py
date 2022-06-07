import unittest

import juego
from bomba import Bomba
from bot import Bot
from jugador import Jugador
from algoritmo import Algoritmo


class MiTest(unittest.TestCase):

    def setUp(self):
        juego.bot_list.append(Bot(11, 11, Algoritmo.DFS))
        juego.jugador = Jugador()

    def test_plant(self):
        bomba = juego.jugador.plantar_bomba(juego.tablero)

        self.assertEqual(1, bomba.posX)
        self.assertEqual(1, bomba.posY)
        self.assertEqual(3, bomba.range)

    def test_get_range(self):

        bomb = juego.jugador.plantar_bomba(juego.tablero)

        self.assertEqual(5, len(bomb.sectors))
        self.assertEqual(True, [1, 1] in bomb.sectors)
        self.assertEqual(True, [1, 2] in bomb.sectors)
        self.assertEqual(True, [2, 1] in bomb.sectors)
        self.assertEqual(True, [1, 3] in bomb.sectors)
        self.assertEqual(True, [3, 1] in bomb.sectors)

        self.assertEqual(False, [1, 0] in bomb.sectors)
        self.assertEqual(False, [0, 1] in bomb.sectors)

    def test_bomb_explode(self):
        temp_bomb = Bomba(3, 11, 11, juego.tablero, juego.bot_list[0])
        juego.bombas.append(temp_bomb)

        juego.actualizar_bombas(2980)

        self.assertEqual(1, len(juego.bombas))
        self.assertEqual(20, temp_bomb.time)

        juego.actualizar_bombas(50)

        self.assertEqual(0, len(juego.bombas))
        self.assertEqual(1, len(juego.explosiones))


if __name__ == '__main__':
    unittest.main()
