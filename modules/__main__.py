from .node import Node
from .open_digraph import open_digraph
from .bool_circ import Bool_circ
from .utils import K_map_prop


if __name__ == '__main__':

    bc = Bool_circ.from_table('1110001000111111')
    #print(K_map_prop('1110001000111111'))
    
    #Bool_circ.parse_parentheses("((x0)|(x1)(x2))|((x1)&(~(x2)))").save_as_dot_file("test.dot")
    #bc = Bool_circ.from_table('1110001000111111')
    print(K_map_prop('1110001000111111'))
    Bool_circ.from_kmap("1110001000111111").save_as_dot_file("dot")
    #bc = Bool_circ.from_table('1110001000111111')
    #K_map_prop("1110001000111111")



    G = Bool_circ.random_bool_circ(6, 5, 8)
    G.display()
