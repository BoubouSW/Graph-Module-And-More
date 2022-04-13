from .bool_circ import Bool_circ


if __name__ == '__main__':
    G = Bool_circ.half_adder(3)
    input = Bool_circ.int_to_bites(0b00010011, n = 8)
    
    input.icompose(G)
    print(input)
    input.evaluate()
    input.save_as_dot_file("test")
