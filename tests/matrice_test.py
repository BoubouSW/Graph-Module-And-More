from modules.matrice import *
import unittest
import sys
import os

root = os.path.normpath(os.path.join(__file__, "./../.."))
sys.path.append(root)  # allows us


class MatriceTest(unittest.TestCase):

    def test_random_int_matrix(self):
        t1 = random_int_matrix(5, True)
        for t in range(5):
            self.assertEqual(t1[t][t], 0)

    def test_random_symetric_int_matrix(self):
        t1 = random_symetric_int_matrix(5, 5)
        for i in range(5):
            for j in range(i):
                self.assertEqual(t1[i][j], t1[j][i])

    def test_random_oriented_int_matrix(self):
        t1 = random_oriented_int_matrix(5, 5)
        for y in range(5):
            for x in range(y):
                if(t1[y][x] != 0):
                    self.assertEqual(t1[x][y], 0)

    def test_random_triangular_int_matrix(self):
        t1 = random_triangular_int_matrix(5, 5)
        for i in range(5):
            for j in range(5):
                if i > j:
                    self.assertEqual(t1[i][j], 0)
