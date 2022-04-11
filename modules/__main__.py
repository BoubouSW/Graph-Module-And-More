from .bool_circ import Bool_circ


if __name__ == '__main__':
    G = Bool_circ.half_adder(3)
    G.save_as_dot_file("adder", verbose=True)
