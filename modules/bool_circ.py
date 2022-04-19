from modules.open_digraph import open_digraph
from modules.node import Node

from modules.bool_circ_mx.bool_circ_construct_mx import Bool_circ_construct_mx
from modules.bool_circ_mx.bool_circ_evaluate_mx import Bool_circ_evaluate_mx


class Bool_circ(open_digraph,
                Bool_circ_construct_mx,
                Bool_circ_evaluate_mx):
    """
    Boolean circuit
    """

    def __init__(self, inputs: list[int], outputs: list[int], nodes: list[Node], passVerif: bool = False):
        super().__init__(inputs, outputs, nodes)
        if not self.is_well_formed() and not passVerif:
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
    def hamming_enc(cls):
        return cls.parse_parentheses("(x0)^(x1)^(x3)", "(x0)^(x2)^(x3)",
                                     "(x0)", "(x1)^(x2)^(x3)", "(x1)",
                                     "(x2)", "(x3)")

    @classmethod
    def hamming_dec(cls):
        top: Bool_circ = cls.parse_parentheses("(x0)^(x2)^(x4)^(x6)", "(x1)^(x2)^(x5)^(x6)",
                                               "(x2)", "(x3)^(x4)^(x5)^(x6)", "(x4)",
                                               "(x5)", "(x6)")
        bottom: Bool_circ = cls.parse_parentheses("((x0)&(x1)&(~(x3)))^(x2)",
                                                  "((x0)&(~(x1))&(x3))^(x4)",
                                                  "((~(x0))&(x1)&(x3))^(x5)", "((x0)&(x1)&(x3))^(x6)")
        return top.compose(bottom)




    def effacement(self, id:int):
        node = self.get_node_by_id(id)
        label = node.get_label
        if label != "1" and label != "0" and label != "&" and label != "|" and label != "~" and label != "^":
            raise ValueError(f"Invalid node")
        child = node.get_children_ids
        if len(child) != 1:
            raise ValueError("Node has more than 1 child")
        if len(self.get_node_by_id(child[0]).get_children_ids) != 0:
            raise ValueError("Child has 1 child")
        for parent in node.get_parent_ids:
            newid = self.add_node("")
            self.add_edge(parent,newid)
        self.remove_nodes_by_id(id,child[0])

    def non_a_travers_xor(self, id:int):
        node = self.get_node_by_id(id)
        label = node.get_label
        if label != "~":
            raise ValueError(f"Invalid node")
        parent = self.get_node_by_id(node.get_parent_ids[0])
        xor = self.get_node_by_id(node.get_children_ids[0])
        self.remove_node_by_id(id)
        self.add_edge(parent.get_id, xor.get_id)
        idno = self.add_node("~")
        child = self.get_node_by_id(xor.get_children_ids[0])
        self.remove_edge(xor.get_id,child.get_id)
        self.add_edge(xor.get_id,idno)
        self.add_edge(idno,child.get_id)