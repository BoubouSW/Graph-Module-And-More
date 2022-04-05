from .node import Node
from .open_digraph import open_digraph
from .bool_circ import Bool_circ
from .utils import K_map_prop


if __name__ == '__main__':
    bc = Bool_circ.from_table('1110001000111111')
    K_map_prop("1110001000111111")