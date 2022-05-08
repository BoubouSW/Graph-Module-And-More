from tabnanny import verbose
from .bool_circ import Bool_circ


if __name__ == '__main__':
    test = Bool_circ.hamming_dec()
    test.save_as_dot_file("test1")
    test.reduction()
    test.save_as_dot_file("test2")
