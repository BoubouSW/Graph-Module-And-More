from random import randrange


def random_int_list(n, bound):
    tab = []
    for i in range(n):
        tab.append(randrange(0, bound))
    return tab


print(random_int_list(5, 10))
