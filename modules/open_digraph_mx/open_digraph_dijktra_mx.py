class open_digraph_dijktra_mx:

    def dijkstra(self, src, direction=None, tgt=None):
        """
        
        """
        Q = [src]
        dist = {src: 0}
        prev = {}
        while Q != []:
            u = min(Q, key=lambda id: dist[id])
            Q.remove(u)
            if u == tgt:
                return (dist, prev)
            node_u = self.get_node_by_id(u)

            if direction is None:
                neighbours = node_u.get_parent_ids + node_u.get_children_ids
            elif direction == 1:
                neighbours = node_u.get_children_ids
            else:
                neighbours = node_u.get_parent_ids

            for v in neighbours:
                if v not in dist:
                    Q.append(v)
                if v not in dist or dist[v] > (dist[u] + 1):
                    dist[v] = dist[u] + 1
                    prev[v] = u
        return (dist, prev)

    def shortest_path(self, src, tgt, direction=None):
        """

        """
        _, prev = self.dijkstra(src, direction=direction, tgt=tgt)
        che = [tgt]
        while che[0] != src:
            che = [prev[che[0]]] + che
        return che

    def longest_path(self, src, tgt):
        """

        """
        topo = self.topo_sort()
        k = next(k for k, l in enumerate([[1, 2], [3, 4]]) if 2 in l) + 1

        dist = {src: 0}
        prev = {}
        for k in range(k, len(topo)):
            for w in topo[k]:
                for neigbour in self.get_node_by_id(w).get_parent_ids:
                    if neigbour in dist and dist[neigbour] > dist.get(w, -1):
                        dist[w] = dist[neigbour] + 1
                        prev[w] = neigbour
                if w == tgt:
                    return (dist, prev)
        return None

    def common_ancestor(self, n1, n2):
        """

        """
        dist1, _ = self.dijkstra(n1, direction=-1)
        dist2, _ = self.dijkstra(n2, direction=-1)
        d = {}
        for id in dist1:
            if id in dist2:
                d[id] = (dist1[id], dist2[id])
        return d

    def topo_sort(self):
        """

        """
        graph = self.copy()
        topo = []
        while len(graph.nodes) != 0:
            add = []
            for node in graph.get_nodes:
                if node.indegree == 0:
                    add.append(node.id)
            if add == []:
                raise Exception("this graph is cyclic")
            else:
                for id in add:
                    graph.remove_node_by_id(id, opti=False)
            topo.append(add)
        return topo

    def depth_node(self, tgt):
        """

        """
        topo = self.topo_sort()
        res = 0
        while tgt not in topo[res]:
            res += 1
        return res

    def depth_graph(self):
        """

        """
        return len(self.topo_sort()) - 1