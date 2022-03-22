from xxlimited import new
from .node import Node
from .open_digraph import open_digraph
from .bool_circ import Bool_circ


if __name__ == '__main__':  # the following code is called only when

    n0 = Node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1})
    n1 = Node(1, 'b', {0: 1}, {2: 2, 5: 1})
    n2 = Node(2, 'c', {0: 1, 1: 2}, {6: 1})

    i0 = Node(3, 'i0', {}, {0: 1})
    i1 = Node(4, 'i1', {}, {0: 1})

    o0 = Node(5, 'o0', {1: 1}, {})
    o1 = Node(6, 'o1', {2: 1}, {})

    G = open_digraph([3, 4], [5, 6], [n0, n1, n2, i0, i1, o0, o1])
    G.add_node("d", {2 : 1}, {})
    G.add_edge(0, 1)
    G.add_edge(7, 2)

    # print(G.is_well_formed())
    # G.remove_node_by_id(1)
    # print(G.is_well_formed())
    # G.remove_node_by_id(5)
    # G.remove_parallel_edge((0,1),(1,2))
    # G.remove_node_by_id(0)
    # G.add_input_node(0)
    # G.add_output_node(7)
    # G.add_output_node(9)
    # print(G.is_well_formed())
    # G.dessine()

    m = [[0, 1, 1, 0, 0],
         [0, 0, 0, 1, 2],
         [0, 0, 0, 2, 0],
         [1, 0, 0, 0, 1],
         [0, 0, 0, 0, 0]]

    Gt: open_digraph = open_digraph.graph_from_adjacency_matrix(m)
    Gt.add_input_node(5)
    #Gt.save_as_dot_file("test", False)
    #Gt2 = open_digraph.from_dot_file("test")
    #Gt2.save_as_dot_file("test2")

    # print(G.adjacency_matrix())
    # print(Gt.adjacency_matrix())

    G2: open_digraph = open_digraph.random(
        1, 1, 1, 1, form="DAG")

    # G2.save_as_dot_file()
    # G2.display()
    G.remove_edge(7, 2)
    #G.save_as_dot_file()

    b1 = Node(1, "&", {5: 1, 3: 1}, {2: 1})
    b2 = Node(2, "|", {1: 1, 3: 1}, {6: 1})
    b3 = Node(3, "", {4: 1}, {1: 1, 2: 1})
    b4 = Node(4, "0", {}, {3: 1})
    b5 = Node(5, "i", {}, {1: 1})
    b6 = Node(6, "o", {2: 1}, {})

    Gb = Bool_circ([5], [6], [b1, b2, b3, b4, b5, b6])
    #Gb.save_as_dot_file("test", True)
    #print(Gb.is_well_formed())
    Gb.min_id()
    Gb.max_id()

    print(G.dijkstra(3,1, tgt = 2))
    print(G.shortest_path(3, 2))
    print(G.common_ancestor(2, 5))
    print(G.topo_sort())
    print(G.longest_path(3, 2))
    G.fusion(3, 4)
    G.save_as_dot_file("dot")

    bool_circ = Bool_circ([], [],[])

    newbool = Bool_circ.parse_parentheses("((x0)&((x1)&(x2)))|((x1)&(~(x2)))")
    print(newbool.is_well_formed())
    newbool.save_as_dot_file(verbose=True)


    #Gb.save_as_dot_file("test1", True)
    #Gb.shift_indices(5)
    #Gb.save_as_dot_file("test2", True)
    #print(Gb)

    #Gb.iparallel(Gb.copy(), Gb.copy())

    #Gb.save_as_dot_file("gb")
    #G2.save_as_dot_file("g2")
    #Gb.icompose(G2)
    #Gb.save_as_dot_file("test")
    #Gb.add_node("0")
    #GBT = Gb.connected_graph()

    #GBT[0].save_as_dot_file("gb0")
    #GBT[1].save_as_dot_file("gb1")

    #print(Gb.is_well_formed())
