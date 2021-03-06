from modules.open_digraph import open_digraph
from modules.node import Node

from modules.bool_circ_mx.bool_circ_construct_mx import Bool_circ_construct_mx
from modules.bool_circ_mx.bool_circ_evaluate_mx import Bool_circ_evaluate_mx
from modules.bool_circ_mx.bool_circ_hamming_mx import Bool_circ_hamming_mx


class Bool_circ(open_digraph,
                Bool_circ_construct_mx,
                Bool_circ_evaluate_mx,
                Bool_circ_hamming_mx):
    """
    Boolean circuit
    """

    def __init__(self, inputs: list[int], outputs: list[int], nodes: list[Node], passVerif: bool = False):
        super().__init__(inputs, outputs, nodes)
        if not self.is_well_formed() and not passVerif:
            raise Exception("this graph is not a bool circ")

    def is_well_formed(self) -> bool:
        """
        check if bool_circ is well formed
        """
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
