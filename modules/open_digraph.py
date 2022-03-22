from dis import dis
from math import dist
import numpy as np

from modules.node import Node
from modules.open_digraph_mx.open_digraph_compositions_mx import open_digrapg_compositions_mx
from modules.open_digraph_mx.open_digraph_get_set_mx import open_digraph_get_set_mx
from modules.open_digraph_mx.open_digraph_display_mx import open_digraph_display_mx
from modules.open_digraph_mx.open_digraph_constructeur_mx import open_digraph_constructeur_mx
from modules.open_digraph_mx.open_digraph_predicate_mx import open_digraph_predicate_mx
from modules.open_digraph_mx.open_digraph_dijktra_mx import open_digraph_dijktra_mx


class open_digraph(
    open_digrapg_compositions_mx,
    open_digraph_get_set_mx,
    open_digraph_display_mx,
    open_digraph_constructeur_mx,
    open_digraph_predicate_mx,
    open_digraph_dijktra_mx
):  # for open directed graph
    """
    data structure for a graph

    Attributes
    ----------
    inputs: int list
        id of input node
    outputs: int list
        id of outputs node
    nodes: <int,Node> dict
        dict with id to nodes
    """

    def __init__(self, inputs: list[int], outputs: list[int], nodes: list):
        """
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        """
        self.inputs: list[int] = inputs
        self.outputs: list[int] = outputs
        self.nodes: dict[int:Node] = {node.id: node for node in nodes}

    ###############
    #   METHODES  #
    ###############

    def copy(self):
        """
        create a copy of the graph
        """
        i = self.inputs.copy()
        o = self.outputs.copy()
        l_n = [node.copy() for node in self.nodes.values()]
        return open_digraph(i, o, l_n)

    def new_id(self) -> int:
        """
        create a new id not used in the graph
        """
        max = 0
        for key in self.nodes.keys():
            if key > max:
                max = key
        return max + 1

    def dict_id_node(self) -> dict[int:int]:
        """
        create a dict with node id and a unique int (id(key):int(value))
        """
        d = dict()
        id = 0
        for key in self.get_node_ids:
            if not (key in self.outputs or key in self.inputs):
                d[key] = id
                id += 1
        return d

    def adjacency_matrix(self) -> list[list[int]]:
        """
        create adjacency matrix of the graph
        """
        d = self.dict_id_node()
        nodes = self.get_nodes
        rm = self.get_input_ids + self.get_output_ids
        mat = np.zeros((len(nodes) - len(rm), len(nodes) - len(rm)), dtype=int)
        for node in nodes:
            if not node.get_id in rm:
                children = node.get_children_ids
                for id in children:
                    if not id in rm:
                        mat[d[node.get_id], d[id]
                            ] = node.get_children_id_mult(id)
        return mat

    def fusion(self, id1:int, id2:int, labelId1:bool=True, label:str=""):
        n1 = self.get_node_by_id(id1)
        if(not labelId1):
            n1.set_label(label)
        n2 = self.get_node_by_id(id2)
        for id in n2.get_children_ids:
            self.add_mult_edge(id1, id, n2.get_children_id_mult(id))
        for id in n2.get_children_ids:
            self.add_mult_edge(id, id1, n2.get_parent_id_mult(id))
        self.remove_node_by_id(id2)
        