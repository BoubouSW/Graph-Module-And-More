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
        self.parents: dict[int:int] = parents
        self.children: dict[int:int] = children

    ##############
    #   GETTERS  #
    ##############

    @property
    def get_id(self) -> int:
        return self.id

    @property
    def get_label(self) -> str:
        return self.label

    @property
    def get_parent_ids(self) -> list[int]:
        return list(self.parents.keys())

    @property
    def get_children_ids(self) -> list[int]:
        return list(self.children.keys())

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

    @property
    def indegree(self) -> int:
        """
        return number of output input
        """
        ind = 0
        for mult in self.parents.values():
            ind += mult
        return ind

    @property
    def outdegree(self):
        """
        return number of output
        """
        out = 0
        for mult in self.children.values():
            out += mult
        return out

    @property
    def degree(self):
        """
        return number of input and output
        """
        return self.indegree + self.outdegree

    ##############
    #   SETTERS  #
    ##############

    def set_id(self, id: int) -> None:
        self.id = id

    def set_label(self, label: str) -> None:
        self.label = label

    def set_parent_ids(self, value: dict[int:int]) -> None:
        self.parents = value

    def set_children_ids(self, value: dict[int:int]) -> None:
        self.children = value

    def add_child_id(self, id: int, value: int) -> None:
        self.children[id] = value

    def add_parent_id(self, id: int, value: int) -> None:
        self.parents[id] = value

    def remove_parent_once(self, id: int) -> None:
        """
        remove one edge with a parent (with his id)
        """
        mult = self.get_parent_id_mult(id)
        if mult > 1:
            self.add_parent_id(id, mult - 1)
        elif mult == 1:
            del self.parents[id]

    def remove_child_once(self, id: int) -> None:
        """
        remove one edge with a child (with his id)
        """
        mult = self.get_children_id_mult(id)
        if mult > 1:
            self.add_child_id(id, mult - 1)
        elif mult == 1:
            del self.children[id]

    def remove_parent_id(self, id: int) -> None:
        """
        remove all edges with a parent (with his id)
        """
        if id in self.parents:
            del self.parents[id]

    def remove_children_id(self, id: int) -> None:
        """
        remove all edges with a child (with his id)
        """
        if id in self.children:
            del self.children[id]

    ###############
    #   METHODES  #
    ###############

    def copy(self):
        """
        create a copy of the node
        """
        return Node(self.id, str(self.label), self.parents.copy(), self.children.copy())

    ################
    #   AFFICHAGE  #
    ################

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
