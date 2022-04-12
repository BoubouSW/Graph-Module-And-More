from .bool_circ import Bool_circ


if __name__ == '__main__':
<<<<<<< HEAD
    #G = Bool_circ.int_to_bites(11)
    G = Bool_circ([], [], [])
    n1 =G.add_node("0")
    n2 = G.add_node('|')
    n3 = G.add_node("1")
    n4 = G.add_node("1")
    n5 = G.add_node("")
    n6 = G.add_node("&")

    G.add_edge(n1, n2)
    G.add_edge(n3, n2)
    G.add_edge(n4, n2)
    G.add_edge(n5, n4)
    G.add_edge(n2, n6)
    G.display()
    G.or_gate(n1)
    G.display("porte")
    

    #print(G.is_well_formed())
    #G.save_as_dot_file("int.dot")
=======
    G = Bool_circ.empty()
    idN = G.add_node("0")
    id1 = G.add_node("1")
    id2 = G.add_node("1")
    idxor = G.add_node("^")
    G.add_edges((idN, idxor), (id1, idxor), (id2, idxor))
    G.add_output_node(idxor)


    G.xor_gate(id1)
    G.save_as_dot_file("test")

>>>>>>> 8e34d77 (add gate)
