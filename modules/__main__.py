from .bool_circ import Bool_circ


if __name__ == '__main__':
    G = Bool_circ.random_bool_circ(6, 5, 8)
    G.display()
