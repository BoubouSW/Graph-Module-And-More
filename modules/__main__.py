from black import TRANSFORMED_MAGICS
from .bool_circ import Bool_circ


if __name__ == '__main__':
    G = Bool_circ.half_adder(2)
    input = Bool_circ.int_to_bites(0b1111, n = 4)
    
    G.save_as_dot_file("adder", verbose=True)
    print(G)
    input.icompose(G)
    input.save_as_dot_file("test1", verbose=True)
    input.evaluate()
    input.save_as_dot_file("test", verbose=True)
