from modules.open_digraph import open_digraph
from modules.node import Node
import unittest


from modules.matrice import random_int_matrix


class DigraphTest(unittest.TestCase):
    def setUp(self):
        self.n0 = Node(0, "a", {3: 1, 4: 1}, {1: 1, 2: 1})
        self.n1 = Node(1, "b", {0: 1}, {2: 2, 5: 1})
        self.n2 = Node(2, "c", {0: 1, 1: 2}, {6: 1})

        self.i0 = Node(3, "i0", {}, {0: 1})
        self.i1 = Node(4, "i1", {}, {0: 1})

        self.o0 = Node(5, "o0", {1: 1}, {})
        self.o1 = Node(6, "o1", {2: 1}, {})

        self.G = open_digraph(
            [3, 4],
            [5, 6],
            [self.n0, self.n1, self.n2, self.i0, self.i1, self.o0, self.o1],
        )

    def test_get_input_ids(self):
        self.assertEqual(self.G.get_input_ids, [3, 4])

    def test_get_output_ids(self):
        self.assertEqual(self.G.get_output_ids, [5, 6])

    def test_get_nodes(self):
        self.assertEqual(
            self.G.get_nodes,
            [self.n0, self.n1, self.n2, self.i0, self.i1, self.o0, self.o1],
        )

    def test_get_node_ids(self):
        self.assertEqual(self.G.get_node_ids, [0, 1, 2, 3, 4, 5, 6])

    def test_get_node_by_id(self):
        self.assertEqual(self.G.get_node_by_id(2), self.n2)

    def test_get_nodes_by_ids(self):
        self.assertEqual(
            self.G.get_nodes_by_ids([0, 1, 2]), [self.n0, self.n1, self.n2]
        )

    def test_set_input_ids(self):
        self.G.set_input_ids([1, 2, 3])
        self.assertEqual(self.G.get_input_ids, [1, 2, 3])

    def test_set_output_ids(self):
        self.G.set_output_ids([4, 5, 6])
        self.assertEqual(self.G.get_output_ids, [4, 5, 6])

    def test_add_input_id(self):
        self.G.add_input_id(8)
        self.assertEqual(8 in self.G.inputs, True)

    def test_add_output_id(self):
        self.G.add_output_id(9)
        self.assertEqual(9 in self.G.outputs, True)

    def test_empty(self):
        self.assertEqual(open_digraph.empty().inputs, [])
        self.assertEqual(open_digraph.empty().outputs, [])
        self.assertEqual(open_digraph.empty().nodes, {})

    def test_new_id(self):
        id_list = self.G.get_node_ids
        new_id = self.G.new_id()
        self.assertFalse(new_id in id_list)

    def test_copy(self):
        dc = self.G.copy()
        self.assertIsNot(dc.inputs, self.G.inputs)
        self.assertIsNot(dc.outputs, self.G.outputs)
        self.assertIsNot(dc.nodes, self.G.nodes)

    def test_add_edge(self):
        self.G.add_edge(1, 2)
        self.assertEqual(self.G.get_node_by_id(1).get_children_id_mult(2), 3)
        self.assertEqual(self.G.get_node_by_id(2).get_parent_id_mult(1), 3)
        self.G.add_edge(2, 1)
        self.assertEqual(self.G.get_node_by_id(2).get_children_id_mult(1), 1)
        self.assertEqual(self.G.get_node_by_id(1).get_parent_id_mult(2), 1)

    def test_add_node(self):
        id = self.G.new_id()
        self.G.add_node(label="d", parents={0: 2}, children={2: 1})
        node_create = self.G.get_node_by_id(id)
        self.assertEqual(node_create.get_label, "d")
        self.assertEqual(node_create.get_id, id)
        self.assertEqual(node_create.get_children_id_mult(2), 1)
        self.assertEqual(node_create.get_parent_id_mult(0), 2)
        self.assertEqual(self.G.get_node_by_id(0).get_children_id_mult(id), 2)
        self.assertEqual(self.G.get_node_by_id(2).get_parent_id_mult(id), 1)
        self.assertTrue(self.G.is_well_formed())

    def test_remove_edge(self):
        self.G.remove_edge(1, 2)
        self.assertEqual(self.G.get_node_by_id(1).get_children_id_mult(2), 1)
        self.assertEqual(self.G.get_node_by_id(2).get_parent_id_mult(1), 1)

        self.G.remove_edge(1, 2)
        self.assertEqual(self.G.get_node_by_id(1).get_children_id_mult(2), 0)
        self.assertEqual(self.G.get_node_by_id(2).get_parent_id_mult(1), 0)

        self.G.remove_edge(1, 2)
        self.assertEqual(self.G.get_node_by_id(1).get_children_id_mult(2), 0)
        self.assertEqual(self.G.get_node_by_id(2).get_parent_id_mult(1), 0)

    def test_remove_parallel_edges(self):
        self.G.remove_parallel_edge(1, 2)
        self.assertTrue(self.G.is_well_formed())
        self.assertEqual(self.G.get_node_by_id(1).get_children_id_mult(2), 0)
        self.assertEqual(self.G.get_node_by_id(2).get_parent_id_mult(1), 0)

        self.G.remove_parallel_edge(1, 2)
        self.assertTrue(self.G.is_well_formed())
        self.assertEqual(self.G.get_node_by_id(1).get_children_id_mult(2), 0)
        self.assertEqual(self.G.get_node_by_id(2).get_parent_id_mult(1), 0)

    def test_remove_node_by_id(self):
        self.G.remove_node_by_id(1)
        self.assertTrue(self.G.is_well_formed)
        self.G.remove_node_by_id(2)
        self.assertTrue(self.G.is_well_formed)
        n = self.G.get_node_by_id(1)
        self.assertEqual(self.G.get_node_by_id(2), None)
        self.assertEqual(n, None)
        nodes = self.G.get_nodes
        for node in nodes:
            self.assertEqual(node.get_children_id_mult(1), 0)
            self.assertEqual(node.get_parent_id_mult(1), 0)
            self.assertEqual(node.get_children_id_mult(2), 0)
            self.assertEqual(node.get_parent_id_mult(2), 0)

    def test_add_input_node(self):
        id = self.G.new_id()
        self.G.add_node(label="t")
        self.G.add_edge(id, 0)
        self.G.add_input_node(id)
        self.assertTrue(self.G.is_well_formed())

    def test_add_output_node(self):
        id = self.G.new_id()
        self.G.add_node(label="t")
        self.G.add_edge(7, id)
        self.G.add_output_node(id)
        self.assertTrue(self.G.is_well_formed())

    def test_is_well_formed(self):
        self.assertTrue(self.G.is_well_formed())
        self.G.remove_node_by_id(1)
        self.assertTrue(self.G.is_well_formed())
        n0 = Node(0, "a", {3: 1, 4: 1}, {1: 1, 2: 1})
        n1 = Node(1, "b", {0: 1}, {2: 2, 5: 1})
        n2 = Node(2, "c", {0: 1, 1: 2}, {6: 1})
        n3 = Node(7, "d", {0: 2}, {})
        n4 = Node(7, "d", {0: 1, 2: 1}, {})
        n5 = Node(7, "d", {}, {0: 2})
        n6 = Node(7, "d", {}, {0: 1, 1: 1})

        i0 = Node(3, "i0", {}, {0: 1})
        i1 = Node(4, "i1", {}, {0: 1})

        o0 = Node(5, "o0", {1: 1}, {})
        o1 = Node(6, "o1", {2: 1}, {})

        Gt = open_digraph([3, 4, 7], [5, 6], [n0, n1, n2, n3, i0, i1, o0, o1])
        self.assertFalse(Gt.is_well_formed())
        Gt = open_digraph([3, 4, 7], [5, 6], [n0, n1, n2, n4, i0, i1, o0, o1])
        self.assertFalse(Gt.is_well_formed())
        Gt = open_digraph([3, 4], [5, 6, 7], [n0, n1, n2, n5, i0, i1, o0, o1])
        self.assertFalse(Gt.is_well_formed())
        Gt = open_digraph([3, 4], [5, 6, 7], [n0, n1, n2, n6, i0, i1, o0, o1])
        self.assertFalse(Gt.is_well_formed())

    def test_matrix(self):
        m = random_int_matrix(5, 5)
        G = open_digraph.graph_from_adjacency_matrix(m)
        adj_m = G.adjacency_matrix()
        for y in range(5):
            for x in range(5):
                self.assertEqual(m[y][x], adj_m[y][x])

    def test_min_id(self):
        self.assertEqual(self.G.min_id(), 0)

    def test_max_id(self):
        self.assertEqual(self.G.max_id(), 6)

    def test_shift_indices(self):
        Gt = self.G.copy()
        Gt.shift_indices(10)
        idG = sorted(self.G.get_node_ids)
        idGt = sorted(Gt.get_node_ids)
        self.assertTrue(self.G.inputs !=
                        Gt.inputs and self.G.outputs != Gt.outputs)
        for i in range(len(idG)):
            self.assertEqual(idGt[i], idG[i] + 10)
        for id in Gt.nodes.keys():
            nodet = Gt.get_node_by_id(id)
            node = self.G.get_node_by_id(id - 10)
            for i in node.get_parent_ids:
                self.assertEqual(nodet.get_parent_id_mult(i),
                                 node.get_parent_id_mult(i - 10))
                self.assertEqual(nodet.get_children_id_mult(i),
                                 node.get_children_id_mult(i - 10))

        Gt.shift_indices(-10)
        self.assertTrue(self.G.inputs ==
                        Gt.inputs and self.G.outputs == Gt.outputs)
        idG = sorted(self.G.get_node_ids)
        idGt = sorted(Gt.get_node_ids)
        for i in range(len(idG)):
            self.assertEqual(idG[i], idGt[i])

    def test_connected_components(self):
        self.assertEqual(self.G.connected_components(),
                         (1, {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}))
        self.G.add_node("a")
        self.assertEqual(self.G.connected_components(),
                         (2, {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 1}))

    def test_iparallel(self):
        Gt = self.G.copy()
        self.G.iparallel(Gt)
        self.assertEqual(self.G.get_input_ids,[10,11,3,4])
        self.assertEqual(self.G.get_output_ids,[12,13,5,6])
        self.assertEqual(self.G.get_node_by_id(9).get_label,"c")
        self.assertEqual(self.G.get_node_by_id(12).get_label,"o0")

    def test_dijktra(self):
        self.assertEqual(self.G.dijkstra(0), ({0: 0, 3: 1, 4: 1, 1: 1, 2: 1, 5: 2, 6: 2}, {
                         3: 0, 4: 0, 1: 0, 2: 0, 5: 1, 6: 2}))
        self.assertEqual(self.G.dijkstra(1), ({1: 0, 0: 1, 2: 1, 5: 1, 3: 2, 4: 2, 6: 2}, {
                         0: 1, 2: 1, 5: 1, 3: 0, 4: 0, 6: 2}))
        self.assertEqual(self.G.dijkstra(3), ({3: 0, 0: 1, 4: 2, 1: 2, 2: 2, 5: 3, 6: 3}, {
                         0: 3, 4: 0, 1: 0, 2: 0, 5: 1, 6: 2}))

    def test_shortest_path(self):
        self.assertEqual(self.G.shortest_path(0, 2), [0, 2])
        self.assertEqual(self.G.shortest_path(1, 5), [1, 5])
        self.assertEqual(self.G.shortest_path(3, 5), [3, 0, 1, 5])

    def test_longest_path(self):
        self.assertEqual(self.G.longest_path(1, 2), [1, 2])
        self.assertEqual(self.G.longest_path(0, 2), [0, 1, 2])

    def test_common_ancestor(self):
        self.assertEqual(self.G.common_ancestor(0, 1), {
                         0: (0, 1), 3: (1, 2), 4: (1, 2)})
        self.assertEqual(self.G.common_ancestor(1, 2), {
                         1: (0, 1), 0: (1, 1), 3: (2, 2), 4: (2, 2)})

    def test_topo_sort(self):
        self.assertEqual(self.G.topo_sort(), [[3, 4], [0], [1], [2, 5], [6]])
        self.G.add_edge(2, 0)
        self.assertRaises(Exception, self.G.topo_sort) 