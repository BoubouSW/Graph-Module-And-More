class open_digraph_predicate_mx:
    def is_well_formed(self) -> bool:
        """
        check if the graph is well formed
        """
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
                if self.get_node_by_id(child).get_parent_id_mult(node.get_id) != mult:
                    return False
            for parent in node.get_parent_ids:
                mult = node.get_parent_id_mult(parent)
                if (
                    self.get_node_by_id(parent).get_children_id_mult(node.get_id)
                    != mult
                ):
                    return False
        return True

    def is_cyclic(self) -> bool:
        """
        check if the graph is cyclic or not
        """
        copy = self.copy()
        while len(copy.nodes) != 0:
            id = None
            for node in copy.get_nodes:
                if node.outdegree == 0:
                    id = node.get_id
            if id == None:
                return True
            else:
                copy.remove_node_by_id(id)
        return False
