from .bool_circ import Bool_circ


if __name__ == '__main__':
    input = Bool_circ.hamming_dec()
    print(input)
    input.save_as_dot_file("test")
