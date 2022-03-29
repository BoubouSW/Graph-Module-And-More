from .node import Node
from .open_digraph import open_digraph
from .bool_circ import Bool_circ


if __name__ == '__main__':
    bc = Bool_circ.from_table('1010')
    bc.save_as_dot_file("dot")