from modules.node import Node


class open_digraph_get_set_mx:
    ##############
    #   GETTERS  #
    ##############
    @property
    def get_input_ids(self) -> list[int]:
        return self.inputs

    @property
    def get_output_ids(self) -> list[int]:
        return self.outputs

    @property
    def get_id_node_map(self) -> dict[int:int]:
        return self.nodes

    @property
    def get_nodes(self) -> list[Node]:
        return list(self.nodes.values())

    @property
    def get_node_ids(self) -> list[int]:
        return list(self.nodes.keys())

    def get_node_by_id(self, k: int) -> Node:
        return self.nodes.get(k, None)

    def get_nodes_by_ids(self, liste: list) -> list[Node]:
        return [self.get_node_by_id(i) for i in liste]

    ##############
    #   SETTERS  #
    ##############
    def set_input_ids(self, value: list[int]) -> None:
        self.inputs = value

    def set_output_ids(self, value: list[int]) -> None:
        self.outputs = value

    def add_input_id(self, id: int) -> None:
        self.inputs.append(id)

    def add_output_id(self, id: int) -> None:
        self.outputs.append(id)

    def add_edge(self, src: int, tgt: int) -> None:
        """
        add an edge between 2 nodes (source -> target)
        """
        id = self.nodes.keys()
        if not (src in id and tgt in id):
            raise (Exception(f"{src} or {tgt} is not in {id}"))
        else:
            src_children_mult = self.nodes[src].get_children_id_mult(tgt)
            tgt_parent_mult = self.nodes[tgt].get_parent_id_mult(src)
            self.nodes[tgt].add_parent_id(src, src_children_mult + 1)
            self.nodes[src].add_child_id(tgt, tgt_parent_mult + 1)

    def add_edges(self, *args) -> None:
        """
        add an edge between 2 nodes (source -> target)
        """
        for src, tgt in args:
            self.add_edge(src, tgt)

    def add_mult_edge(self, src: int, tgt: int, mult: int) -> None:
        """
        add {mult} edges between 2 nodes (source -> target)
        """
        id = self.nodes.keys()
        if not (src in id and tgt in id):
            raise (Exception())
        else:
            src_children_mult = self.nodes[src].get_children_id_mult(tgt)
            tgt_parent_mult = self.nodes[tgt].get_parent_id_mult(src)
            self.nodes[tgt].add_parent_id(src, src_children_mult + mult)
            self.nodes[src].add_child_id(tgt, tgt_parent_mult + mult)

    def add_node(
        self, label: str = "", parents: dict[int:int] = {}, children: dict[int: int] = {}
    ) -> None:
        """
        add a node to the graph linked to parents and children (list of id)
        """
        id = self.new_id()
        self.nodes[id] = Node(id, label, {}, {})
        for parent_id in parents.keys():
            self.add_mult_edge(parent_id, id, parents[parent_id])
        for child_id in children.keys():
            self.add_mult_edge(id, child_id, children[child_id])
        return id

    def remove_edge(self, src: int, tgt: int) -> None:
        """
        remove an edge between 2 nodes (source -> target)
        """
        self.get_node_by_id(src).remove_child_once(tgt)
        self.get_node_by_id(tgt).remove_parent_once(src)

    def remove_edges(self, *args: list[(int, int)]) -> None:
        """
        remove edges between a list of 2 nodes ([src,tgt],[src,tgt],...)
        """
        for arg in args:
            src, tgt = arg
            self.remove_edge(src, tgt)

    def remove_parallel_edge(self, src: int, tgt: int) -> None:
        """
        remove all edges between 2 nodes (source -> target)
        """
        self.get_node_by_id(src).remove_children_id(tgt)
        self.get_node_by_id(tgt).remove_parent_id(src)

    def remove_parallel_edges(self, *args: list[(int, int)]) -> None:
        """
        remove all edges between a list of 2 nodes ([src,tgt],[src,tgt],...)
        """
        for arg in args:
            src, tgt = arg
            self.remove_parallel_edge(src, tgt)

    def remove_node_by_id(self, id: int, opti: bool = True) -> None:
        """
        remove a node of the graph by his id
        delete input/output if this node is linked to one
        """
        node = self.get_node_by_id(id)

        for child in node.get_children_ids:
            self.remove_parallel_edge(id, child)
            n: Node = self.get_node_by_id(child)
            if n.get_id in self.get_output_ids and opti:
                self.remove_node_by_id(child)

        for parent in node.get_parent_ids:
            self.remove_parallel_edge(parent, id)
            n: Node = self.get_node_by_id(parent)
            if n.get_id in self.get_input_ids and opti:
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

    def remove_nodes_by_id(self, *args: int) -> None:
        """
        remove a list of nodes of the graph by their id (id1, id2,...)
        """
        for id in args:
            self.remove_node_by_id(id)

    def add_input_node(self, id: int, label: str = "i") -> None:
        """
        add an input node linked to a node (with his id)
        """
        if id in self.get_input_ids:
            raise (Exception("can't add input on input"))
        new_id = self.add_node(label=label, children={id: 1})
        inputs = self.get_input_ids
        inputs.append(new_id)
        self.set_input_ids(inputs)

    def add_output_node(self, id: int, label: str = "o") -> None:
        """
        add an output node linked to a node (with his id)
        """
        if id in self.get_output_ids:
            raise (Exception("can't add output on output"))
        new_id = self.add_node(label=label, parents={id: 1})
        output = self.get_output_ids
        output.append(new_id)
        self.set_output_ids(output)
