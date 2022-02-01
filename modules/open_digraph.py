import igraph as ig


class Node:
    """
    Node: represents a node in a graph

    Attributes
    ----------
    id: int
    label: str
    parents: <int,int> dict
    children: <int,int> dict
    """

    def __init__(self, identity: int, label: str, parents: dict, children: dict):
        """
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        """
        self.id: int = identity
        self.label: str = label
        self.parents: dict[int: int] = parents
        self.children: dict[int: int] = children

    def __str__(self) -> str:
        str_ret = "\tI :"
        for id in self.parents.keys():
            str_ret += f" {id}"
        str_ret += f"\n\tid = {self.id}\n"
        str_ret += f"\tlabel = {self.label}\n"
        str_ret += f"\tO :"
        for id in self.children.keys():
            str_ret += f" {id}"
        str_ret += "\n\n"
        return str_ret

    def __repr__(self) -> str:
        str_ret = "I :"
        for id in self.parents.keys():
            str_ret += f" {id}"
        str_ret += f"\nid = {self.id}\n"
        str_ret += f"label = {self.label}\n"
        str_ret += f"O :"
        for id in self.children.keys():
            str_ret += f" {id}"
        return str_ret

    @property
    def get_id(self) -> int:
        return self.id

    @property
    def get_label(self) -> str:
        return self.label

    @property
    def get_parent_ids(self) -> list[int]:
        tab = []
        for p in self.parents.keys():
            tab.append(p)
        return tab

    @property
    def get_children_ids(self) -> list[int]:
        tab = []
        for p in self.children.keys():
            tab.append(p)
        return tab

    def get_children_id_mult(self, id: int) -> int:
        if id in self.children:
            return self.children[id]
        else:
            return 0

    def get_parent_id_mult(self, id: int) -> int:
        if id in self.parents:
            return self.parents[id]
        else:
            return 0

    def set_id(self, id: int) -> None:
        self.id = id

    def set_label(self, label: str) -> None:
        self.label = label

    def set_parent_ids(self, value: dict[int: int]) -> None:
        self.parents = value

    def set_children_ids(self, value: dict[int: int]) -> None:
        self.children = value

    def add_child_id(self, id: int, value: int) -> None:
        self.children[id] = value

    def add_parent_id(self, id: int, value: int) -> None:
        self.parents[id] = value

    def copy(self):
        return Node(self.id, str(self.label), self.parents.copy(), self.children.copy())

    def remove_parent_once(self, id: int) -> None:
        mult = self.get_parent_id_mult(id)
        if mult > 1:
            self.add_parent_id(id, mult - 1)
        elif mult == 1:
            del self.parents[id]

    def remove_child_once(self, id: int) -> None:
        mult = self.get_children_id_mult(id)
        if mult > 1:
            self.add_child_id(id, mult - 1)
        elif mult == 1:
            del self.children[id]

    def remove_parent_id(self, id: int) -> None:
        if id in self.parents:
            del self.parents[id]

    def remove_children_id(self, id: int) -> None:
        if id in self.children:
            del self.children[id]


class open_digraph:  # for open directed graph
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

    def __init__(self, inputs: list, outputs: list, nodes: list):
        """
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        """
        self.inputs: list[int] = inputs
        self.outputs: list[int] = outputs
        # self.nodes: <int,node> dict
        self.nodes: dict[int: Node] = {node.id: node for node in nodes}

    def __str__(self) -> str:
        str_ret = f"I = {self.inputs}\n"
        for node in self.nodes.values():
            if not (node.get_id in self.inputs or node.get_id in self.outputs):
                str_ret += str(node)
        str_ret += f"O = {self.outputs}\n"
        return str_ret

    def __repr__(self) -> str:
        return str(self)

    @property
    def get_input_ids(self) -> list[int]:
        return self.inputs

    @property
    def get_output_ids(self) -> list[int]:
        return self.outputs

    @property
    def get_id_node_map(self) -> dict[int: int]:
        return self.nodes

    @property
    def get_nodes(self) -> list[Node]:
        tab = []
        for k in self.nodes.values():
            tab.append(k)
        return tab

    @property
    def get_node_ids(self) -> list[int]:
        tab = []
        for k in self.nodes.keys():
            tab.append(k)
        return tab

    def get_node_by_id(self, k: int) -> Node:
        if k in self.nodes:
            return self.nodes[k]
        else:
            return None

    def get_nodes_by_ids(self, liste: list) -> list[Node]:
        tab = []
        for i in liste:
            tab.append(self.get_node_by_id(i))
        return tab

    def set_input_ids(self, value: list[int]) -> None:
        self.inputs = value

    def set_output_ids(self, value: list[int]) -> None:
        self.outputs = value

    def add_input_id(self, id: int) -> None:
        self.inputs.append(id)

    def add_output_id(self, id: int) -> None:
        self.outputs.append(id)

    def new_id(self) -> int:
        max = 0
        for key in self.nodes.keys():
            if key > max:
                max = key
        return max + 1

    @classmethod
    def empty(cls):
        return cls([], [], [])

    def copy(self):
        i = self.inputs.copy()
        o = self.outputs.copy()
        l_n = [node for node in self.nodes.values()]
        return open_digraph(i, o, l_n)

    def add_edge(self, src: int, tgt: int) -> None:
        id = self.nodes.keys()
        if not (src in id and tgt in id):
            raise (Exception())
        else:
            src_children_mult = self.nodes[src].get_children_id_mult(tgt)
            tgt_parent_mult = self.nodes[tgt].get_parent_id_mult(src)
            self.nodes[tgt].add_parent_id(src, src_children_mult + 1)
            self.nodes[src].add_child_id(tgt, tgt_parent_mult + 1)

    def add_node(self, label: str = "",
                 parents: list[int] = [],
                 children: list[int] = []) -> None:
        id = self.new_id()
        self.nodes[id] = Node(id, label, {}, {})
        for parent_id in parents:
            self.add_edge(parent_id, id)
        for child_id in children:
            self.add_edge(id, child_id)
        return id

    def remove_edge(self, src: int, tgt: int) -> None:
        self.get_node_by_id(src).remove_child_once(tgt)
        self.get_node_by_id(tgt).remove_parent_once(src)

    def remove_edges(self, *args: list[(int, int)]) -> None:
        for arg in args:
            src, tgt = arg
            self.remove_edge(src, tgt)

    def remove_parallel_edge(self, src: int, tgt: int) -> None:
        self.get_node_by_id(src).remove_children_id(tgt)
        self.get_node_by_id(tgt).remove_parent_id(src)

    def remove_parallel_edges(self, *args: list[(int, int)]) -> None:
        for arg in args:
            src, tgt = arg
            self.remove_parallel_edge(src, tgt)

    def remove_node_by_id(self, id: int) -> None:
        node = self.get_node_by_id(id)

        for child in node.get_children_ids:
            self.remove_parallel_edge(id, child)
            n: Node = self.get_node_by_id(child)
            if(n.get_id in self.get_output_ids):
                self.remove_node_by_id(child)

        for parent in node.get_parent_ids:
            self.remove_parallel_edge(parent, id)
            n: Node = self.get_node_by_id(parent)
            if(n.get_id in self.get_input_ids):
                self.remove_node_by_id(parent)

        if id in self.get_input_ids:
            inputs = self.get_input_ids
            inputs.remove(id)
            self.set_input_ids(inputs)

        if id in self.get_output_ids:
            outputs = self.get_output_ids
            outputs.remove(id)
            self.set_output_ids(outputs)
        self.nodes.pop(id)

    def remove_nodes_by_id(self, *args: list[(int, int)]) -> None:
        for id in args:
            self.remove_node_by_id(id)

    def is_well_formed(self) -> bool:
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
                if(self.get_node_by_id(child)
                   .get_parent_id_mult(node.get_id) != mult):
                    return False
            for parent in node.get_parent_ids:
                mult = node.get_parent_id_mult(parent)
                if(self.get_node_by_id(parent)
                   .get_children_id_mult(node.get_id) != mult):
                    return False
        return True

    def add_input_node(self, id: int) -> None:
        if id in self.get_input_ids:
            raise (Exception("can't add input on input"))
        new_id = self.add_node(label="i", children=[id])
        inputs = self.get_input_ids
        inputs.append(new_id)
        self.set_input_ids(inputs)

    def add_output_node(self, id: int) -> None:
        if id in self.get_output_ids:
            raise(Exception("can't add output on output"))
        new_id = self.add_node(label="o", parents=[id])
        output = self.get_output_ids
        output.append(new_id)
        self.set_output_ids(output)

    def dessine(self, name: str = "mygraph") -> None:
        """
        Il y a besoin de la librarie "igraph"
        La fonction génère un fichier .dot qu'on peut ensuite
        visualiser à l'aide de divers outils
        (en l'occurence on utilise l'extension "Graphviz" sur vscode)
        """
        nodes = self.get_nodes                        
        ipt = self.get_input_ids                      
        opt = self.get_output_ids                      
        g = ig.Graph(directed=True)
        g.add_vertices(len(nodes))
        ids = self.get_node_ids
        id_tab = dict()

        for i in range(len(ids)):
            id_tab[ids[i]] = i
            g.vs[i]["id"] = ids[i]
            g.vs[i]["label"] = nodes[i].label
            if ids[i] in ipt:
                g.vs[i]["color"] = "red"
            elif ids[i] in opt:
                g.vs[i]["color"] = "green"
            elif not (ids[i] in ipt and ids[i] in opt):
                g.vs[i]["color"] = "black"

        for node in nodes:
            for idc in node.get_children_ids:
                for i in range(node.get_children_id_mult(idc)):
                    g.add_edge(id_tab[node.get_id], id_tab[idc])

        g.write(name + ".dot")
