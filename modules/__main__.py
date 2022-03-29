from .node import Node
from .open_digraph import open_digraph
from .bool_circ import Bool_circ
from .utils import K_map


if __name__ == '__main__':
    bc = Bool_circ.from_table('1110001000111111')
    print(K_map('1110001000111111'))