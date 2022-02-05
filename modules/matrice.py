from random import randint
import numpy as np


def random_int_list(n: int, bound: int) -> list[int]:
    """
    return a random n list with int in [0, bound] 
    """
    return np.random.randint(bound + 1, size=(n))


def random_int_matrix(n: int, bound: int,
                      null_diag: bool = True) -> list[list[int]]:
    """
    return a random n * n matrix with int in [0, bound] 
    """
    a = np.random.randint(bound + 1, size=(n, n))
    if(null_diag):
        np.fill_diagonal(a, 0)
    return a


def random_symetric_int_matrix(n: int, bound: int,
                               null_diag=True) -> list[list[int]]:
    """
    return a random n * n symetric matrix with int in [0, bound] 
    """
    m = random_int_matrix(n, bound, null_diag)
    return (m * m.T) // 2


def random_oriented_int_matrix(n, bound, null_diag=True):
    """
    return a random n * n matrix with int in [0, bound] 
    who represet an oriented graph
    """
    mat = random_int_matrix(n, bound, null_diag)
    for y in range(n):
        for x in range(y):
            if mat[x][y] != 0 and mat[y][x] != 0:
                if randint(0, 1) == 0:
                    mat[y][x] = 0
                else:
                    mat[x][y] = 0
    return mat


def random_triangular_int_matrix(n, bound, null_diag=True):
    mat = random_int_matrix(n, bound, null_diag)
    for i in range(n):
        for j in range(n):
            if i > j:
                mat[i][j] = 0
    return mat
