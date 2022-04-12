from .bool_circ import Bool_circ


if __name__ == '__main__':
    G = Bool_circ.int_to_bites(11)
    G.save_as_dot_file("int.dot")
