from numpy import ma
import igraph as ig


class Node:
    """
    Doc de la classe Node à compléter ...
    """

    def __init__(self, identity: int, label: str, parents: dict, children: dict):
        """
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        """
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children

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
    def get_id(self):
        return self.id

    @property
    def get_label(self):
        return self.label

    @property
    def get_parent_ids(self):
        tab = []
        for p in self.parents.keys():
            tab.append(p)
        return tab

    @property
    def get_children_ids(self):
        tab = []
        for p in self.children.keys():
            tab.append(p)
        return tab

    def get_children_id_mult(self, id):
        if id in self.children:
            return self.children[id]
        else:
            return 0

    def get_parent_id_mult(self, id):
        if id in self.parents:
            return self.parents[id]
        else:
            return 0

    def set_id(self, id):
        self.id = id

    def set_label(self, label):
        self.label = label

    def set_parent_ids(self, value):
        self.parents = value

    def set_children_ids(self, value):
        self.children = value

    def add_child_id(self, id, value):
        self.children[id] = value

    def add_parent_id(self, id, value):
        self.parents[id] = value

    def copy(self):
        return Node(self.id, str(self.label), self.parents.copy(), self.children.copy())


class open_digraph:  # for open directed graph
    """
    Doc de la classe open_digraph à compléter ...
    """

    def __init__(self, inputs: list, outputs: list, nodes: list):
        """
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        """
        self.inputs = inputs
        self.outputs = outputs
        # self.nodes: <int,node> dict
        self.nodes = {node.id: node for node in nodes}

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
    def get_input_ids(self):
        return self.inputs

    @property
    def get_output_ids(self):
        return self.outputs

    @property
    def get_id_node_map(self):
        return self.nodes

    @property
    def get_nodes(self):
        tab = []
        for k in self.nodes.values():
            tab.append(k)
        return tab

    @property
    def get_node_ids(self):
        tab = []
        for k in self.nodes.keys():
            tab.append(k)
        return tab

    def get_node_by_id(self, k: int):
        return self.nodes[k]

    def get_nodes_by_ids(self, liste: list):
        tab = []
        for i in liste:
            tab.append(self.get_node_by_id(i))
        return tab

    def set_input_ids(self, value):
        self.inputs = value

    def set_output_ids(self, value):
        self.outputs = value

    def add_input_id(self, id):
        self.inputs.append(id)

    def add_output_id(self, id):
        self.outputs.append(id)

    def new_id(self):
        max = 0
        for key in self.nodes.keys():
            if key > max:
                max = key
        return key + 1

    @classmethod
    def empty(cls):
        return cls([], [], [])

    def copy(self):
        i = self.inputs.copy()
        o = self.outputs.copy()
        l_n = [node for node in self.nodes.values()]
        return open_digraph(i, o, l_n)

    def add_edge(self, src, tgt):
        id = self.nodes.keys()
        if not (src in id and tgt in id):
            raise (Exception())
        else:
            src_children_mult = self.nodes[src].get_children_id_mult(tgt)
            tgt_parent_mult = self.nodes[tgt].get_parent_id_mult(src)
            self.nodes[tgt].add_parent_id(src, src_children_mult + 1)
            self.nodes[src].add_child_id(tgt, tgt_parent_mult + 1)

    def add_node(self, label="", parents=[], children=[]):
        id = self.new_id()
        self.nodes[id] = Node(id, label, {}, {})
        for parent_id in parents:
            self.add_edge(parent_id, id)
        for child_id in children:
            self.add_edge(id, child_id)

    def dessine(self, name="mygraph"):

        nodes = self.get_nodes
        ipt = self.get_input_ids
        opt = self.get_output_ids
        g = ig.Graph(directed=True)
        g.add_vertices(len(nodes))
        ids = self.get_node_ids

        for i in range(len(ids)):
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
                    g.add_edge(node.get_id, idc)

        g.write(name + ".dot")
