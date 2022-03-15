import numpy as np

from modules.node import Node
from modules.open_digraph_mx.open_digraph_compositions_mx import (
    open_digrapg_compositions_mx,
)
from modules.open_digraph_mx.open_digraph_get_set_mx import open_digraph_get_set_mx
from modules.open_digraph_mx.open_digraph_display_mx import open_digraph_display_mx
from modules.open_digraph_mx.open_digraph_constructeur_mx import (
    open_digraph_constructeur_mx,
)


class open_digraph(
    open_digrapg_compositions_mx,
    open_digraph_get_set_mx,
    open_digraph_display_mx,
    open_digraph_constructeur_mx,
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
        (doesn't work yet)
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
                        mat[d[node.get_id], d[id]] = node.get_children_id_mult(id)
        return mat

    def dijkstra(self, src, direction=None):
        Q = [src]
        dist = {src: 0}
        prev = {}
        while Q != []:
            u = min(Q, key=lambda x: x.get_id)
            Q.remove(u)
            neighbours = []
            for v in neighbours:
                if not v in dist:
                    Q.append(v)
                if not v in dist or dist[v] > (dist[u] + 1):
                    dist[v] = dist[u] + 1
                    prev[v] = u
        return (dist, prev)

    ################
    #   PREDICATS  #
    ################

    def is_well_formed(self) -> bool:
        """
        check if the graph is well formed
        """
        inputs = self.get_input_ids
        outputs = self.get_output_ids
        nodes_id = self.get_node_ids
        for i in inputs:
            if not (i in nodes_id):
                return False
            child = self.get_node_by_id(i).get_children_ids
            if (
                self.get_node_by_id(i).get_parent_ids != []
                or len(child) != 1
                or self.get_node_by_id(i).get_children_id_mult(child[0]) != 1
            ):
                return False

        for o in outputs:
            if not (o in nodes_id):
                return False
            parent = self.get_node_by_id(o).get_parent_ids
            if (
                self.get_node_by_id(o).get_children_ids != []
                or len(parent) != 1
                or self.get_node_by_id(o).get_parent_id_mult(parent[0]) != 1
            ):
                return False

        for id in nodes_id:
            if id != self.get_node_by_id(id).get_id:
                return False

        for node in self.get_nodes:
            for child in node.get_children_ids:
                mult = node.get_children_id_mult(child)
                if self.get_node_by_id(child).get_parent_id_mult(node.get_id) != mult:
                    return False
            for parent in node.get_parent_ids:
                mult = node.get_parent_id_mult(parent)
                if (
                    self.get_node_by_id(parent).get_children_id_mult(node.get_id)
                    != mult
                ):
                    return False
        return True

    def is_cyclic(self) -> bool:
        copy = self.copy()
        while len(copy.nodes) != 0:
            id = None
            for node in copy.get_nodes:
                if node.outdegree == 0:
                    id = node.get_id
            if id == None:
                return True
            else:
                copy.remove_node_by_id(id)
        return False
