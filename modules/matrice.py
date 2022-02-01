from random import randrange

from matplotlib.image import NonUniformImage


def random_int_list(n, bound):
    return [randrange(0, bound) for _ in range(n)]

