class Node:
    def __init__(self, identity: int, label: str, parents: dict, children: dict):
        '''
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        '''
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
        return [p.id for p in self.parents]

    @property
    def get_children_ids(self):
        return [p.id for p in self.children]

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
        return Node(self.id, str(self.label),
                    self.parents.copy(),
                    self.children.copy())


class open_digraph:  # for open directed graph
    def __init__(self, inputs: list, outputs: list, nodes: list):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        self.inputs = inputs
        self.outputs = outputs
        # self.nodes: <int,node> dict
        self.nodes = {node.id: node for node in nodes}

    def __str__(self) -> str:
        str_ret = f"I = {self.inputs}\n"
        for node in self.nodes.values():
            if(not(node.get_id in self.inputs or
               node.get_id in self.outputs)):
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
        return self.nodes.values()

    @property
    def get_node_ids(self):
        return self.nodes.keys()

    @property
    def get_node_by_id(self, k: int):
        return self.nodes[k]

    @property
    def get_nodes_by_ids(self, liste: list):
        tab = []
        for i in liste:
            tab.append(self.get_node_by_id(i))
        return tab

    def set_input_ids(self, value):
        self.inputs = value

    def set_output_ids(self, value):
        self.outputs = value

    def add_input_ids(self, id, value):
        self.inputs[id] = value

    def add_output_id(self, id, value):
        self.output[id] = value

    @classmethod
    def empty(cls):
        return cls([], [], [])

    def copy(self):
        i = self.inputs.copy()
        o = self.outputs.copy()
        l_n = [node for node in self.nodes.values()]
        return open_digraph(i, o, l_n)
