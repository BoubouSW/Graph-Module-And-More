from .bool_circ import Bool_circ


if __name__ == '__main__':
    G = Bool_circ.adder(2)
    

    G.save_as_dot_file("test", verbose=True)

