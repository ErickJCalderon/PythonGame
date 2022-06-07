import unittest
import juego

from bot import Bot
from jugador import Jugador
from algoritmo import Algoritmo


class MiTest(unittest.TestCase):

    def setUp(self):
        juego.bot_list.append(Bot(11, 11, Algoritmo.BFS))
        juego.bot_list.append(Bot(1, 11, Algoritmo.BFS))
        juego.jugador = Jugador()

    def test_explosion_sectors(self):

        enemigo = juego.bot_list[0]
        juego.bombas.append(enemigo.plantar_bomba(juego.tablero))
        juego.actualizar_bombas(2980)
        juego.actualizar_bombas(50)

        self.assertEqual(1, len(juego.explosiones))
        exp = juego.explosiones[0]

        self.assertEqual(5, len(exp.sectors))
        self.assertEqual(True, [11, 11] in exp.sectors)
        self.assertEqual(True, [11, 10] in exp.sectors)
        self.assertEqual(True, [10, 11] in exp.sectors)
        self.assertEqual(True, [11, 9] in exp.sectors)
        self.assertEqual(True, [9, 11] in exp.sectors)

        self.assertEqual(False, [11, 12] in exp.sectors)
        self.assertEqual(False, [12, 11] in exp.sectors)

    def test_box_destroy(self):

        juego.tablero[2][1] = 2
        self.assertEqual(2, juego.tablero[2][1])
        juego.bombas.append(juego.jugador.plantar_bomba(juego.tablero))
        juego.actualizar_bombas(2980)
        juego.actualizar_bombas(50)

        self.assertEqual(0, juego.tablero[2][1])
        self.assertEqual(True, [2, 1] in juego.explosiones[0].sectors)

    def test_death(self):
        en = juego.bot_list[1]
        juego.bombas.append(en.plantar_bomba(juego.tablero))
        juego.actualizar_bombas(1500)
        self.assertEqual(True, en.life)
        self.assertEqual(0, len(juego.explosiones))

        juego.actualizar_bombas(1501)
        self.assertEqual(False, en.life)
        self.assertEqual(0, len(juego.explosiones))


if __name__ == '__main__':
    unittest.main()
