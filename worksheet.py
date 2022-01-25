from modules.open_digraph import *

if __name__ == '__main__':  # the following code is called only when

    n0 = Node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1})
    n1 = Node(1, 'b', {0: 1}, {2: 2, 5: 1})
    n2 = Node(2, 'c', {0: 1, 1: 2}, {6: 1})

    i0 = Node(3, 'i0', {}, {0: 1})
    i1 = Node(4, 'i1', {}, {0: 1})

    o0 = Node(5, 'o0', {1: 1}, {})
    o1 = Node(6, 'o1', {2: 1}, {})

    G = open_digraph([3, 4], [5, 6], [n0, n1, n2, i0, i1, o0, o1])
    G.add_node("d", [2], [])
    G.add_edge(0, 1)
    G.add_edge(7, 2)

    #G.remove_node_by_id(1)
    
    print(G.is_well_formed())

    G.dessine()
