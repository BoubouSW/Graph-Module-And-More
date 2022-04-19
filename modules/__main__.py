from .bool_circ import Bool_circ


if __name__ == '__main__':
    test = Bool_circ.empty()
    xor1 = test.add_node("")
    xor2 = test.add_node("^")
    test.add_edge(xor1, xor2)
    test.add_edge(xor1, xor2)
    test.add_input_node(xor1)
    test.add_input_node(xor2)
    test.add_input_node(xor2)
    test.xor_involution(xor1)
    test.save_as_dot_file("test")
