from .bool_circ import Bool_circ


if __name__ == '__main__':
    test = Bool_circ.hamming_dec()
    test.reduction()
    test.save_as_dot_file("test")
