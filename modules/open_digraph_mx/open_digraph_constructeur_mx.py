import re

from random import randint

import modules.matrice as mat

class open_digraph_constructeur_mx:
    ####################
    #   CONSTRUCTEURS  #
    ####################

    @classmethod
    def empty(cls):
        """
        create an empty graph
        """
        return cls([], [], [])

    @classmethod
    def graph_from_adjacency_matrix(cls, matrix: list[list[int]]):
        """
        defined graph with matrix
        """
        G = cls.empty()
        for i in range(len(matrix)):
            G.add_node("n" + str(i + 1))
            G.add_mult_edge(i + 1, i + 1, matrix[i][i])
            for j in range(i):
                G.add_mult_edge(i + 1, j + 1, matrix[i][j])
                G.add_mult_edge(j + 1, i + 1, matrix[j][i])
        return G

    @classmethod
    def random(
        cls, n: int, bound: int, inputs: int = 0, outputs: int = 0, form: str = "free"
    ):
        """
        create a random graph with n nodes with inputs and outputs that you want
        you can choose an form of graph :
        - free
        - DAG
        - oriented
        - loop-free
        - undirected
        - loop-free undirected
        """
        if form == "free":
            G = cls.graph_from_adjacency_matrix(
                mat.random_int_matrix(n, bound, False))
        elif form == "DAG":
            G = cls.graph_from_adjacency_matrix(
                mat.random_triangular_int_matrix(n, bound, True)
            )
        elif form == "oriented":
            G = cls.graph_from_adjacency_matrix(
                mat.random_oriented_int_matrix(n, bound, False)
            )
        elif form == "loop-free":
            G = cls.graph_from_adjacency_matrix(
                mat.random_int_matrix(n, bound, True))
        elif form == "undirected":
            G = cls.graph_from_adjacency_matrix(
                mat.random_triangular_int_matrix(n, bound, False)
            )
        elif form == "loop-free undirected":
            G = cls.graph_from_adjacency_matrix(
                mat.random_triangular_int_matrix(n, bound, True)
            )

        nodes = G.get_node_ids
        for _ in range(inputs):
            G.add_input_node(nodes[randint(0, len(nodes) - 1)])
        for _ in range(outputs):
            G.add_output_node(nodes[randint(0, len(nodes) - 1)])

        return G

    @classmethod
    def from_dot_file(cls, path: str):
        G = cls.empty()
        with open(f"{path}.dot") as dot:
            line = dot.readline()
            labels = re.findall(r"label=\"(\w+)", line)
            for label in labels:
                G.add_node(label=label)

            inputs = re.findall(r"id=(\d),label=\w*,color=r", line)
            for id in inputs:
                G.add_input_id(int(id))
            output = re.findall(r"id=(\d),label=\w*,color=g", line)
            for id in output:
                G.add_output_id(int(id))
            nodes = re.findall(r"(?:(\d)->(\d))", line)
            for src, tgt in nodes:
                G.add_edge(int(src), int(tgt))
        return G

