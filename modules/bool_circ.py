import math

from modules.open_digraph import open_digraph
from modules.node import Node
import modules.utils as ut


class Bool_circ(open_digraph):
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
    def parse_parentheses(cls, *args):
        g = cls.empty()
        oper = ["&", "|", "~", "^", "0", "1", ""]
        inputDiv = {}
        for i, s in enumerate(args):
            o = g.add_node(f"o{i}")
            n = g.add_node(f"")
            g.add_edge(n, o)
            g.add_output_id(o)
            current_node = g.get_node_by_id(n)
            s2 = ""
            for char in s:
                if char == '(':
                    current_node.set_label(current_node.get_label + s2)
                    id = g.add_node('', {}, {})
                    g.add_edge(id, current_node.id)
                    current_node = g.get_node_by_id(id)
                    s2 = ""
                elif char == ')':
                    current_node.set_label(current_node.get_label + s2)
                    if current_node.label not in oper:
                        if current_node.label in inputDiv:
                            idDiv = inputDiv[current_node.label]
                            g.add_edge(idDiv, current_node.get_children_ids[0])
                            g.remove_node_by_id(current_node.id)
                            current_node = g.get_node_by_id(idDiv)
                        else:
                            idDiv = g.add_node("")
                            g.add_edge(
                                idDiv, current_node.get_children_ids[-1])
                            g.remove_edge(current_node.id,
                                          current_node.get_children_ids[-1])
                            g.add_edge(current_node.id, idDiv)
                            g.add_input_id(current_node.id)
                            inputDiv[current_node.label] = idDiv
                            current_node = g.get_node_by_id(idDiv)
                    current_node = g.get_node_by_id(
                        current_node.get_children_ids[-1])
                    s2 = ""
                else:
                    s2 += char
        return g

    @classmethod
    def from_table(cls, bits: str):
        nbVar = math.log2(len(bits))
        if not nbVar.is_integer():
            raise Exception("this table is not a boolean table")
        G = cls.empty()
        idsSplit = []
        for i in range(int(nbVar)):
            idSplit = G.add_node("")
            G.add_input_node(idSplit, label=f"I{i}")
            idsSplit.append(idSplit)

        outputid = G.add_node("|", {}, {})
        G.add_output_node(outputid)
        for line, bit in enumerate(bits):
            if bit == "1":
                idAnd = G.add_node("&")
                G.add_edge(idAnd, outputid)
                line = bin(line)[2:]
                line = "0" * (int(nbVar) - len(line)) + line
                for i, bitEntry in enumerate(line):
                    if(bitEntry == "1"):
                        G.add_edge(idsSplit[i], idAnd)
                    else:
                        idNon = G.add_node("~")
                        G.add_edge(idNon, idAnd)
                        G.add_edge(idsSplit[i], idNon)
        return G
    
    @classmethod()
    def from_kmap(cls, bits: str):
        return cls.parse_parentheses(ut.K_map_prop(bits))
