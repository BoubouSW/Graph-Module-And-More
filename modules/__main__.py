from .bool_circ import Bool_circ


if __name__ == '__main__':
    G = Bool_circ.half_adder(2)
    input = Bool_circ.int_to_bites(0b1110, n = 4)
    
    input.icompose(G)
    input.evaluate()
    input.save_as_dot_file("test")
