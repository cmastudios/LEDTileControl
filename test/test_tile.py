from unittest import TestCase

from tile import Tile


class TestTile(TestCase):
    def test_index(self):
        tile1 = Tile(3, 3)
        self.assertEqual(0, tile1.index(0, 0))
        self.assertEqual(1, tile1.index(1, 0))
        self.assertEqual(2, tile1.index(2, 0))
        self.assertEqual(5, tile1.index(0, 1))
        self.assertEqual(4, tile1.index(1, 1))
        self.assertEqual(3, tile1.index(2, 1))
        self.assertEqual(6, tile1.index(0, 2))
        self.assertEqual(7, tile1.index(1, 2))
        self.assertEqual(8, tile1.index(2, 2))
        tile2 = Tile(10, 10)
        self.assertEqual(0, tile2.index(0, 0))
        self.assertEqual(9, tile2.index(9, 0))
        self.assertEqual(19, tile2.index(0, 1))
        self.assertEqual(10, tile2.index(9, 1))
        self.assertEqual(20, tile2.index(0, 2))
        self.assertEqual(29, tile2.index(9, 2))
        self.assertEqual(99, tile2.index(0, 9))
        self.assertEqual(90, tile2.index(9, 9))
        tile3 = Tile(10, 3)
        self.assertEqual(0, tile3.index(0, 0))
        self.assertEqual(9, tile3.index(9, 0))
        self.assertEqual(19, tile3.index(0, 1))
        self.assertEqual(10, tile3.index(9, 1))
        self.assertEqual(20, tile3.index(0, 2))
        self.assertEqual(29, tile3.index(9, 2))
