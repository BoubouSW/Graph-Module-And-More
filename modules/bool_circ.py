from modules.open_digraph import open_digraph
from modules.node import Node


class Bool_circ(open_digraph):
    """
    Boolean circuit
    """

    def __init__(self, inputs: list[int], outputs: list[int], nodes: list[Node]):
        super().__init__(inputs, outputs, nodes)
        if not self.is_well_formed():
            raise Exception("this graph is not a bool circ")

    def is_well_formed(self) -> bool:
        cond = {
            "": lambda out, ind: ind == 1,
            "&": lambda out, ind: out == 1,
            "|": lambda out, ind: out == 1,
            "^": lambda out, ind: out == 1,
            "~": lambda out, ind: ind == 1 and out == 1,
            "0": lambda out, ind: ind == 0,
            "1": lambda out, ind: ind == 0,
        }
        inputs = self.get_input_ids
        outputs = self.get_output_ids
        if self.is_cyclic():
            return False
        for node in self.get_nodes:
            if not(node.id in inputs or node.id in outputs):
                if node.label in cond.keys():
                    if(not(cond[node.label](node.outdegree, node.indegree))):
                        return False
                else:
                    return False
        return True

    @classmethod
    def parse_parentheses(cls,s):
        n0 = Node(1,"",{},{0:1})
        o = Node(0," ",{1:1},{})
        g = open_digraph([], [0], [n0,o])
        current_node = n0
        s2 = ""
        for char in s:
            if char == '(':
                current_node.set_label(current_node.get_label + s2)
                id = g.add_node('',{},{})
                g.add_edge(id, current_node.id)
                current_node = g.get_node_by_id(id)
                s2 = ""
            elif char == ')':
                current_node.set_label(current_node.get_label + s2)
                current_node = g.get_node_by_id(current_node.get_children_ids[0])
                s2 = ""
            else:
                s2 += char
        return g



