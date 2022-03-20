from dis import dis
from math import dist
import numpy as np

from modules.node import Node
from modules.open_digraph_mx.open_digraph_compositions_mx import open_digrapg_compositions_mx
from modules.open_digraph_mx.open_digraph_get_set_mx import open_digraph_get_set_mx
from modules.open_digraph_mx.open_digraph_display_mx import open_digraph_display_mx
from modules.open_digraph_mx.open_digraph_constructeur_mx import open_digraph_constructeur_mx
from modules.open_digraph_mx.open_digraph_predicate_mx import open_digraph_predicate_mx


class open_digraph(
    open_digrapg_compositions_mx,
    open_digraph_get_set_mx,
    open_digraph_display_mx,
    open_digraph_constructeur_mx,
    open_digraph_predicate_mx
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
                        mat[d[node.get_id], d[id]
                            ] = node.get_children_id_mult(id)
        return mat

    def dijkstra(self, src, direction=None, tgt=None):
        Q = [src]
        dist = {src: 0}
        prev = {}
        while Q != []:
            u = min(Q, key=lambda id: dist[id])
            Q.remove(u)
            if u == tgt:
                return (dist, prev)
            node_u = self.get_node_by_id(u)

            if direction is None:
                neighbours = node_u.get_parent_ids + node_u.get_children_ids
            elif direction == 1:
                neighbours = node_u.get_children_ids
            else:
                neighbours = node_u.get_parent_ids

            for v in neighbours:
                if v not in dist:
                    Q.append(v)
                if v not in dist or dist[v] > (dist[u] + 1):
                    dist[v] = dist[u] + 1
                    prev[v] = u
        return (dist, prev)

    def shortest_path(self, src, tgt, direction=None):
        _, prev = self.dijkstra(src, direction=direction, tgt=tgt)
        che = [tgt]
        while che[0] != src:
            che = [prev[che[0]]] + che
        return che

    def longest_path(self, src, tgt):
        topo = self.topo_sort()
        k = next(k for k, l in enumerate([[1, 2], [3, 4]]) if 2 in l) + 1

        dist = {src: 0}
        prev = {}
        for k in range(k, len(topo)):
            for w in topo[k]:
                for neigbour in self.get_node_by_id(w).get_parent_ids:
                    if neigbour in dist and dist[neigbour] > dist.get(w, -1):
                        dist[w] = dist[neigbour] + 1
                        prev[w] = neigbour
                if w == tgt:
                    return (dist, prev)
        return None

    def common_ancestor(self, n1, n2):
        dist1, _ = self.dijkstra(n1, direction=-1)
        dist2, _ = self.dijkstra(n2, direction=-1)
        d = {}
        for id in dist1:
            if id in dist2:
                d[id] = (dist1[id], dist2[id])
        return d

    def topo_sort(self):
        graph = self.copy()
        topo = []
        while len(graph.nodes) != 0:
            add = []
            for node in graph.get_nodes:
                if node.indegree == 0:
                    add.append(node.id)
            if add == []:
                raise Exception("this graph is cyclic")
            else:
                for id in add:
                    graph.remove_node_by_id(id, opti=False)
            topo.append(add)
        return topo

    def depth_node(self, tgt):
        topo = self.topo_sort()
        res = 0
        while tgt not in topo[res]:
            res += 1
        return res

    def depth_graph(self):
        return len(self.topo_sort()) - 1
