from tokenize import String


class node:
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
        return f"id = {self.id}"

    @property
    def get_id(self):
        return self.id

    @property
    def get_label(self):
        return self.label


class open_digraph:  # for open directed graph
    def __init__(self, inputs: int, outputs: int, nodes: dict):
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
        return f"""inputs = {self.inputs}
outputs = {self.outputs}
nodes = {[str(node) for node in self.nodes]}
        """
