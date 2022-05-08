from modules import Node


class Bool_circ_hamming_mx:
    def effacement(self, id: int):
        node = self.get_node_by_id(id)
        label = node.get_label
        if label not in ["1", "0", "&", "|", "~", "^"]:
            raise ValueError(f"Invalid node")
        child = node.get_children_ids
        if len(child) != 1:
            raise ValueError("Node has more than 1 child")
        if len(self.get_node_by_id(child[0]).get_children_ids) != 0:
            raise ValueError("Child has 1 child")
        for parent in node.get_parent_ids:
            newid = self.add_node("")
            self.add_edge(parent, newid)
        self.remove_nodes_by_id(id, child[0])

    def non_a_travers_xor(self, id: int):
        node = self.get_node_by_id(id)
        label = node.get_label
        if label != "~":
            raise ValueError(f"Invalid node")
        parent = self.get_node_by_id(node.get_parent_ids[0])
        xor = self.get_node_by_id(node.get_children_ids[0])
        self.remove_node_by_id(id)
        self.add_edge(parent.get_id, xor.get_id)
        idno = self.add_node("~")
        child = self.get_node_by_id(xor.get_children_ids[0])
        self.remove_edge(xor.get_id, child.get_id)
        self.add_edge(xor.get_id, idno)
        self.add_edge(idno, child.get_id)

    def xor_associativ(self, id: int):
        xorNode1 = self.get_node_by_id(id)
        if(xorNode1.get_label != "^"):
            raise ValueError(f"{id} is not a ^")
        xorNode2 = self.get_node_by_id(xorNode1.get_children_ids[0])
        if(xorNode2.get_label != "^"):
            raise ValueError(f"{xorNode2.get_id} is not a ^")
        for node in xorNode1.get_parent_ids:
            self.add_edge(node, xorNode2.get_id)
        self.remove_node_by_id(id, opti=False)

    def xor_involution(self, id: int):
        splitNode: Node = self.get_node_by_id(id)
        if(splitNode.get_label != ""):
            raise ValueError(f"{id} is not a spliter node")
        change = False
        for child_id in splitNode.get_children_ids:
            trans = self.get_node_by_id(child_id)
            if trans.get_label == '^':
                change = True
                print(child_id, "OK", id)
                for _ in range(splitNode.get_children_id_mult(child_id)):
                    self.remove_edge(id, child_id)

    def copy_associativ(self, id: int):
        splitNode = self.get_node_by_id(id)
        if(splitNode.get_label != ""):
            raise ValueError(f"{id} is not a spliter node")
        for idChild in splitNode.get_children_ids:
            nodeChild = self.get_node_by_id(idChild)
            if nodeChild.get_label == "":
                for child in nodeChild.get_children_ids:
                    for _ in range(
                            nodeChild.get_children_id_mult(child)):
                        self.add_edges((id, child))
                self.remove_node_by_id(idChild, opti=False)

    def non_a_travers_copie(self, id: int):
        node = self.get_node_by_id(id)
        if node.get_label != "~":
            raise ValueError(f"Invalid node")
        idco = node.get_children_ids[0]
        copie = self.get_node_by_id(idco)
        if copie.get_label != "":
            raise ValueError(f"Not a copie")
        for child in copie.get_children_ids:
            newid = self.add_node("~")
            self.remove_edge(idco, child)
            self.add_edge(idco, newid)
            self.add_edge(newid, child)
        self.add_edge(node.get_parent_ids[0], idco)
        self.remove_node_by_id(id)

    def involution_non(self, id: int):
        node = self.get_node_by_id(id)
        if node.get_label != "~":
            raise ValueError(f"Invalid node")
        idparent = node.get_parent_ids[0]
        idno = node.get_children_ids[0]
        no = self.get_node_by_id(idno)
        if no.get_label != "~":
            raise ValueError(f"Not a not")
        idchild = no.get_children_ids[0]
        self.remove_nodes_by_id(id, idno)
        self.add_edge(idparent, idchild)

    def reduction(self):
        modify = True
        while modify:
            modify = False
            for node in self.get_node_ids:
                nodeObj = self.get_node_by_id(node)
                if nodeObj != None and nodeObj.get_children_ids:
                    if nodeObj.label == "^":
                        nodeChild = nodeObj.get_children_ids[0]
                        if self.get_node_by_id(nodeChild).get_label == "^":
                            self.xor_associativ(node)
                            modify = True
                    elif nodeObj.label == "~":
                        nodeChild = nodeObj.get_children_ids[0]
                        if self.get_node_by_id(nodeChild).get_label == "^":
                            self.non_a_travers_xor(node)
                            modify = True
                        elif self.get_node_by_id(nodeChild).get_label == "":
                            self.non_a_travers_copie(node)
                            modify = True
                        elif self.get_node_by_id(nodeChild).get_label == "~":
                            self.involution_non(node)
                            modify = True
                    elif nodeObj.label == "":
                        for child in nodeObj.get_children_ids:
                            if self.get_node_by_id(child) != None:
                                continue
                            if self.get_node_by_id(child).get_label == "^":
                                self.xor_involution(node)
                                modify = True
                            elif self.get_node_by_id(child).get_label == "":
                                self.copy_associativ(node)
                                modify = True
                    if nodeObj.label in ["1", "0", "&", "|", "~", "^"]:
                        if len(nodeObj.get_children_ids) == 1:
                            childObj = self.get_node_by_id(
                                nodeObj.get_children_ids[0])
                            if (childObj.get_label == ""
                                    and not childObj.get_children_ids):
                                self.effacement(node)
                                modify = True

                    if len(nodeObj.get_children_ids) == 0:
                        self.remove_node_by_id(node)
                        modify = True
                    elif ((nodeObj.get_label not in ["0", "1"] or
                           nodeObj.get_children_ids[0] not in self.get_output_ids
                           ) and len(nodeObj.get_parent_ids) == 0
                          and node not in self.get_input_ids):
                        print(self.get_node_by_id(node).get_label)
                        self.switch_gate(node)
                        modify = True
