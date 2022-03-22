from modules import Node, open_digraph

import unittest

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