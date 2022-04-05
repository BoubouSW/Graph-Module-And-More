from .node import Node
from .open_digraph import open_digraph
from .bool_circ import Bool_circ
from .utils import K_map_prop


if __name__ == '__main__':
    G = Bool_circ.random_bool_circ(6, 5, 8)
    G.display()
