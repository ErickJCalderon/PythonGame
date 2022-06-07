import unittest
import juego


class MiTest(unittest.TestCase):

    def test_map_generation_corners(self):
        juego.generar_mapa()
        self.assertEqual(0, juego.tablero[1][1])
        self.assertEqual(0, juego.tablero[1][2])
        self.assertEqual(0, juego.tablero[2][1])

        l = len(juego.tablero)

        self.assertEqual(0, juego.tablero[l - 2][1])
        self.assertEqual(0, juego.tablero[l - 2][2])
        self.assertEqual(0, juego.tablero[l - 3][1])

        self.assertEqual(0, juego.tablero[1][l - 2])
        self.assertEqual(0, juego.tablero[1][l - 3])
        self.assertEqual(0, juego.tablero[2][l - 2])

        self.assertEqual(0, juego.tablero[l - 2][l - 2])
        self.assertEqual(0, juego.tablero[l - 2][l - 3])
        self.assertEqual(0, juego.tablero[l - 3][l - 2])


if __name__ == '__main__':
    unittest.main()

