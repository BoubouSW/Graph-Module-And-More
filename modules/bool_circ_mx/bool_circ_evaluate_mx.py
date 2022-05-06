class Bool_circ_evaluate_mx:
    
    def __copy_gate(self, id: int):
        node = self.get_node_by_id(id)
        if node.get_label != "1" and node.get_label != "0":
            raise ValueError(f"Invalid node {id}")
        idco = node.get_children_ids[0]
        copy = self.get_node_by_id(idco)
        if copy.get_label != '':
            raise ValueError(f"Invalid node {copy.get_id}")
        for child in copy.get_children_ids:
            n = self.add_node(node.get_label)
            self.add_edge(n, child)
        self.remove_nodes_by_id(id, idco, opti=False)

    def __and_gate(self, id: int):
        node = self.get_node_by_id(id)
        label = node.get_label
        if label != "1" and label != "0":
            raise ValueError(f"Invalid node {id}")
        idet = node.get_children_ids[0]
        et = self.get_node_by_id(idet)
        if et.get_label != '&':
            raise ValueError(f"Invalid node {et.get_id}")
        if label == "0":
            for parent in et.get_parent_ids:
                if parent != id:
                    n = self.add_node('')
                    self.add_edge(parent, n)
                    self.remove_edge(parent, idet)
            et.set_label("0")
            self.remove_nodes_by_id(id, opti=False)
        if label == "1":
            self.remove_node_by_id(id)

    def __or_gate(self, id: int):
        node = self.get_node_by_id(id)
        label = node.get_label
        if label != "1" and label != "0":
            raise ValueError(f"Invalid node {n.get_children_ids[0]}")
        idou = node.get_children_ids[0]
        ou = self.get_node_by_id(idou)
        if ou.get_label != '|':
            raise ValueError(f"Invalid node {ou.get_id}")
        if label == "1":
            for parent in ou.get_parent_ids:
                if parent != id:
                    n = self.add_node('')
                    self.add_edge(parent, n)
                    self.remove_edge(parent, idou)
            ou.set_label("1")
            self.remove_nodes_by_id(id, opti=False)
        if label == "0":
            self.remove_node_by_id(id)

    def __not_gate(self, id) -> None:
        n = self.get_node_by_id(id)
        if(self.get_node_by_id(n.get_children_ids[0]).get_label != "~"):
            raise ValueError(f"Invalid node {n.get_children_ids[0]}")
        node_not = self.get_node_by_id(n.get_children_ids[0])
        if(n.get_label == "0"):
            node_not.set_label("1")
        elif(n.get_label == "1"):
            node_not.set_label("0")
        else:
            raise ValueError(f"Invalid node {id}")
        self.remove_nodes_by_id(id)

    def __neutral_gate(self, id: int) -> None:
        n = self.get_node_by_id(id)
        if len(n.get_parent_ids) > 0:
            raise ValueError(f"Invalid node {id}")
        if (n.get_label == "|" or n.get_label == "^"):
            n.set_label("0")
        elif n.get_label == "&":
            n.set_label("1")
        else:
            raise ValueError(f"Invalid node {id}")

    def __xor_gate(self, id: int) -> None:
        n = self.get_node_by_id(id)
        if self.get_node_by_id(n.get_children_ids[0]).get_label != "^":
            raise ValueError(f"Invalid node {n.get_children_ids[0]}")
        if n.get_label == "1":
            xor = self.get_node_by_id(n.get_children_ids[0])
            idNot = self.add_node("~")
            self.add_edges((xor.get_id, idNot),
                           (idNot, xor.get_children_ids[0]))
            self.remove_edge(xor.get_id, xor.get_children_ids[0])

        elif n.get_label != "0":
            raise ValueError(f"Invalid node {id}")

        self.remove_nodes_by_id(id)

    def switch_gate(self, id: int) -> None:
        """
        check which gate it is
        """
        node = self.get_node_by_id(id)
        if node.label in ['&', '|', '^']:
            self.__neutral_gate(id)
        else:
            children = node.get_children_ids
            if len(children) != 1:
                return
            label = self.get_node_by_id(children[0]).get_label
            if label == '':
                self.__copy_gate(id)
            elif label == '&':
                self.__and_gate(id)
            elif label == '|':
                self.__or_gate(id)
            elif label == '~':
                self.__not_gate(id)
            elif label == '^':
                self.__xor_gate(id)

    def evaluate(self) -> None:
        """
        simplifies the graph from the above rules
        """
        change = True
        while change:
            change = False
            for id in self.get_node_ids:
                n = self.get_node_by_id(id)
                if n != None and n.get_parent_ids:
                    if n.get_children_ids:
                        self.remove_node_by_id(id)
                        continue
                    if ((n.get_label != "0" and n.get_label != "1") or
                       n.get_children_ids[0] not in self.get_output_ids):
                        self.switch_gate(id)
                        change = True
