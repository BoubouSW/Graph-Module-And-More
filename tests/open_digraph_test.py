from modules.open_digraph import *
import unittest
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us


class InitTest(unittest.TestCase):
    def test_init_node(self):
        n0 = node(0, 'i', {}, {1: 1})
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, 'i')
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1: 1})
        self.assertIsInstance(n0, node)

    def test_init_digraph(self):
        d0 = open_digraph([], [], [])
        self.assertEqual(d0.inputs, [])
        self.assertEqual(d0.nodes, {})
        self.assertEqual(d0.outputs, [])


class NodeTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'a', [], [1])

    def test_get_id(self):
        self.assertEqual(self.n0.get_id, 0)

    def test_get_label(self):
        self.assertEqual(self.n0.get_label, 'a')


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run0, node)
