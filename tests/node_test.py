import unittest

from modules.node import Node


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
