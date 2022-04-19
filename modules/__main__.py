from .bool_circ import Bool_circ


if __name__ == '__main__':
    
    #input = Bool_circ.hamming_dec()
    #print(input)
    #input.save_as_dot_file("test")

    G = Bool_circ.empty()
    n1 = G.add_node("^")
    n2 = G.add_node("a")
    n3 = G.add_node("b")
    n4 = G.add_node("c")
    n5 = G.add_node("~")
    n6 = G.add_node("")
    
    G.add_edge(n2, n1)
    G.add_edge(n3, n1)
    G.add_edge(n4, n5)
    G.add_edge(n5, n1)
    G.add_edge(n1, n6)

    G.non_a_travers_xor(n5)
    G.display()
