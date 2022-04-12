from .bool_circ import Bool_circ


if __name__ == '__main__':
    G = Bool_circ.empty()
    idN = G.add_node("0")
    id1 = G.add_node("1")
    id2 = G.add_node("1")
    idxor = G.add_node("^")
    G.add_edges((idN, idxor), (id1, idxor), (id2, idxor))
    G.add_output_node(idxor)


    G.xor_gate(id1)
    G.save_as_dot_file("test")

