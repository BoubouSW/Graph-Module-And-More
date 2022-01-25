from traceback import print_tb
from modules.open_digraph import *
import unittest
import sys
import os

root = os.path.normpath(os.path.join(__file__, "./../.."))
sys.path.append(root)  # allows us


class InitTest(unittest.TestCase):
    def test_init_node(self):
        n0 = Node(0, "i", {}, {1: 1})
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, "i")
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1: 1})
        self.assertIsInstance(n0, Node)

    def test_init_digraph(self):
        d0 = open_digraph([], [], [])
        self.assertEqual(d0.inputs, [])
        self.assertEqual(d0.nodes, {})
        self.assertEqual(d0.outputs, [])


class NodeTest(unittest.TestCase):
    def setUp(self):
        self.n0 = Node(0, "a", {1: 1}, {1: 2, 2: 1, 3: 1})

    def test_get_id(self):
        self.assertEqual(self.n0.get_id, 0)

    def test_get_label(self):
        self.assertEqual(self.n0.get_label, "a")

    def test_get_parent_ids(self):
        self.assertEqual(self.n0.get_parent_ids, [1])

    def test_get_children_ids(self):
        self.assertEqual(self.n0.get_children_ids, [1, 2, 3])

    def test_get_children_id_mult(self):
        self.assertEqual(self.n0.get_children_id_mult(1), 2)
        self.assertEqual(self.n0.get_children_id_mult(2), 1)
        self.assertEqual(self.n0.get_children_id_mult(3), 1)
        self.assertEqual(self.n0.get_children_id_mult(4), 0)

    def test_set_id(self):
        self.n0.set_id(7)
        self.assertEqual(self.n0.get_id, 7)

    def test_set_label(self):
        self.n0.set_label("h")
        self.assertEqual(self.n0.get_label, "h")

    def test_set_parent_ids(self):
        self.n0.set_parent_ids({5: 2, 1: 4, 3: 1})
        self.assertEqual(self.n0.get_parent_ids, [5, 1, 3])

    def test_set_children_ids(self):
        self.n0.set_children_ids({1: 4, 6: 3, 2: 1})
        self.assertEqual(self.n0.get_children_ids, [1, 6, 2])

    def test_add_child_id(self):
        self.n0.add_child_id(4, 2)
        self.assertEqual(self.n0.children, {1: 2, 2: 1, 3: 1, 4: 2})

    def test_add_parent_id(self):
        self.n0.add_parent_id(2, 2)
        self.assertEqual(self.n0.parents, {1: 1, 2: 2})

    def test_copy(self):
        nc = self.n0.copy()
        self.assertIsNot(nc.label, self.n0.id)
        nc.label = "b"
        self.assertIsNot(nc.label, self.n0.label)
        self.assertIsNot(nc.parents, self.n0.parents)
        self.assertIsNot(nc.children, self.n0.children)

    def test_remove_parent_once(self):
        self.n0.remove_parent_once(1)
        self.assertEqual(self.n0.get_parent_id_mult(1), 0)
        self.assertFalse(1 in self.n0.parents)

        self.n0.add_parent_id(2, 2)
        self.n0.remove_parent_once(2)
        self.assertEqual(self.n0.get_parent_id_mult(2), 1)

        self.n0.remove_parent_once(1)
        self.assertEqual(self.n0.get_parent_id_mult(1), 0)
        self.assertFalse(1 in self.n0.parents)

    def test_remove_child_once(self):
        self.n0.remove_child_once(1)
        self.assertEqual(self.n0.get_children_id_mult(1), 1)

        self.n0.remove_child_once(1)
        self.assertEqual(self.n0.get_children_id_mult(1), 0)
        self.assertFalse(1 in self.n0.children)

        self.n0.remove_child_once(1)
        self.assertEqual(self.n0.get_children_id_mult(1), 0)
        self.assertFalse(1 in self.n0.children)

    def test_remove_parent_id(self):
        self.n0.remove_parent_id(1)
        self.assertEqual(self.n0.get_parent_id_mult(1), 0)
        self.assertFalse(1 in self.n0.parents)

        self.n0.remove_parent_id(1)
        self.assertEqual(self.n0.get_parent_id_mult(1), 0)
        self.assertFalse(1 in self.n0.parents)

    def test_remove_children_id(self):
        self.n0.remove_children_id(1)
        self.assertEqual(self.n0.get_children_id_mult(1), 0)
        self.assertFalse(1 in self.n0.children)

        self.n0.remove_children_id(3)
        self.assertEqual(self.n0.get_children_id_mult(3), 0)
        self.assertFalse(3 in self.n0.children)


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
        self.G.add_node(label='d', parents=[0, 0], children=[2])
        node_create = self.G.get_node_by_id(id)
        self.assertEqual(node_create.get_label, 'd')
        self.assertEqual(node_create.get_id, id)
        self.assertEqual(node_create.get_children_id_mult(2), 1)
        self.assertEqual(node_create.get_parent_id_mult(0), 2)
        self.assertEqual(self.G.get_node_by_id(0).get_children_id_mult(id), 2)
        self.assertEqual(self.G.get_node_by_id(2).get_parent_id_mult(id), 1)

    def test_remove_edge(self):
        self.G.remove_edge(1, 2)
        self.assertEqual(self.G.get_node_by_id(1)
                         .get_children_id_mult(2), 1)
        self.assertEqual(self.G.get_node_by_id(2)
                         .get_parent_id_mult(1), 1)

        self.G.remove_edge(1, 2)
        self.assertEqual(self.G.get_node_by_id(1)
                         .get_children_id_mult(2), 0)
        self.assertEqual(self.G.get_node_by_id(2)
                         .get_parent_id_mult(1), 0)

        self.G.remove_edge(1, 2)
        self.assertEqual(self.G.get_node_by_id(1)
                         .get_children_id_mult(2), 0)
        self.assertEqual(self.G.get_node_by_id(2)
                         .get_parent_id_mult(1), 0)

    def test_remove_parallel_edges(self):
        self.G.remove_parallel_edge(1, 2)
        self.assertEqual(self.G.get_node_by_id(1)
                         .get_children_id_mult(2), 0)
        self.assertEqual(self.G.get_node_by_id(2)
                         .get_parent_id_mult(1), 0)

        self.G.remove_parallel_edge(1, 2)
        self.assertEqual(self.G.get_node_by_id(1)
                         .get_children_id_mult(2), 0)
        self.assertEqual(self.G.get_node_by_id(2)
                         .get_parent_id_mult(1), 0)


if __name__ == "__main__":  # the following code is called only when
    unittest.main()  # precisely this file is run0, node)
