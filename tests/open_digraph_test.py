from modules.open_digraph import *
import unittest
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us


class InitTest(unittest.TestCase):
    def test_init_node(self):
        n0 = Node(0, 'i', {}, {1: 1})
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, 'i')
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
        self.n0 = Node(0, 'a', [], [1])

    def test_get_id(self):
        self.assertEqual(self.n0.get_id, 0)

    def test_get_label(self):
        self.assertEqual(self.n0.get_label, 'a')

    def test_copy(self):
        nc = self.n0.copy()
        self.assertIsNot(nc.label, self.n0.id)
        nc.label = 'b'
        self.assertIsNot(nc.label, self.n0.label)
        self.assertIsNot(nc.parents, self.n0.parents)
        self.assertIsNot(nc.children, self.n0.children)


class Digraph(unittest.TestCase):
    def setUp(self):
        n0 = Node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1})
        n1 = Node(1, 'b', {0: 1}, {2: 2, 5: 1})
        n2 = Node(2, 'c', {0: 1, 1: 2}, {6: 1})

        i0 = Node(3, 'i0', {}, {0: 1})
        i1 = Node(4, 'i1', {}, {0: 1})

        o0 = Node(5, 'o0', {1: 1}, {})
        o1 = Node(6, 'o1', {2: 1}, {})

        self.G = open_digraph([3, 4], [5, 6], [n0, n1, n2, i0, i1, o0, o1])
    
    def test_empty(self):
        self.assertEqual(open_digraph.empty().inputs , [])
        self.assertEqual(open_digraph.empty().outputs , [])
        self.assertEqual(open_digraph.empty().nodes , {})
    
    def test_copy(self):
        dc = self.G.copy()
        self.assertIsNot(dc.inputs, self.G.inputs)
        self.assertIsNot(dc.outputs, self.G.outputs)
        self.assertIsNot(dc.nodes, self.G.nodes)


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run0, node)
