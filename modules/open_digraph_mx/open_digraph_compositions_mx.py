class open_digrapg_compositions_mx:

    def min_id(self) -> int:
        nodes = self.get_node_ids
        if nodes == []:
            raise Exception("pas de noeuds")
        mini = nodes[0]
        for i in nodes:
            if i < mini:
                mini = i
        return mini

    def max_id(self):
        nodes = self.get_node_ids
        if nodes == []:
            raise Exception("pas de noeuds")
        maxi = nodes[0]
        for i in nodes:
            if i > maxi:
                maxi = i
        return maxi

    def shift_indices(self, n: int):
        """ 
        add n for every id
        """
        self.set_input_ids([i + n for i in self.get_input_ids])
        self.set_output_ids([i + n for i in self.get_output_ids])
        for i in sorted(self.get_node_ids, reverse=n > 0):
            node = self.get_node_by_id(i)
            node.set_id(node.get_id + n)
            node.set_children_ids(
                {n + ch: node.get_children_id_mult(ch) for ch in node.children.keys()})
            node.set_parent_ids(
                {n + ch: node.get_parent_id_mult(ch) for ch in node.parents.keys()})
            del self.nodes[i]
            self.nodes[i + n] = node

    def iparallel(self, *args) -> None:
        """
        add g to self
        """
        for g in args:
            print(g.max_id())
            self.shift_indices(g.max_id() + 1)
            for i in g.get_input_ids:
                self.add_input_id(i)
            for o in g.get_output_ids:
                self.add_output_id(o)
            for id in g.get_node_ids:
                self.nodes[id] = g.get_node_by_id(id).copy()

    def parallel(self, *args):
        """
        return g add self
        """
        Gt = self.copy()
        for arg in args:
            Gt.iparallel(arg)
        return Gt

    def icompose(self, g) -> None:
        """
        do composition with g and self
        """
        if(len(self.get_output_ids) != len(g.get_input_ids)):
            raise ValueError
        else:
            self.shift_indices(g.max_id())
            for id in g.get_node_ids:
                self.nodes[id] = g.get_node_by_id(id).copy()
            for ouput, input in zip(self.get_output_ids, g.get_input_ids):
                self.add_edge(self.get_node_by_id(ouput).get_parent_ids[0],
                              g.get_node_by_id(input).get_children_ids[0])
                self.remove_node_by_id(ouput)
                self.remove_node_by_id(input)
            self.set_output_ids(g.get_output_ids)

    def compose(self, g):
        Gt = self.copy()
        Gt.icompose(g)
        return Gt

    def __connected_components(self, dict_node, nb_connex, id_acc):
        dict_node[id_acc] = nb_connex
        node = self.get_node_by_id(id_acc)
        for id in node.get_children_ids:
            if(not id in dict_node):
                self.__connected_components(dict_node, nb_connex, id)
        for id in node.get_parent_ids:
            if(not id in dict_node):
                self.__connected_components(dict_node, nb_connex, id)

    def connected_components(self):
        """
        return number of connected graph and associate 
        id with connected graph
        """
        dict_node = dict()
        nb_connex = 0
        for node in self.get_node_ids:
            if(not node in dict_node):
                self.__connected_components(dict_node, nb_connex, node)
                nb_connex += 1

        return (nb_connex, dict_node)

    def split(self):
        """
        Construct list with connected graph
        """
        nb, connected = self.connected_components()
        graphs = [self.empty() for _ in range(nb)]
        for node in connected:
            graph = connected[node]
            graphs[graph].nodes[node] = self.get_node_by_id(node).copy()
            if node in self.inputs:
                graphs[graph].add_input_id(node)
            elif node in self.outputs:
                graphs[graph].add_output_id(node)
        return graphs
