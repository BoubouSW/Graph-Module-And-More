import math
from random import randint
from modules.open_digraph import open_digraph
from modules.node import Node
import modules.utils as ut


class Bool_circ(open_digraph):
    """
    Boolean circuit
    """

    def __init__(self, inputs: list[int], outputs: list[int], nodes: list[Node], passVerif: bool = False):
        super().__init__(inputs, outputs, nodes)
        if not self.is_well_formed() and not passVerif:
            raise Exception("this graph is not a bool circ")

    def is_well_formed(self) -> bool:
        cond = {
            "": lambda out, ind: ind == 1,
            "&": lambda out, ind: out == 1,
            "|": lambda out, ind: out == 1,
            "^": lambda out, ind: out == 1,
            "~": lambda out, ind: ind == 1 and out == 1,
            "0": lambda out, ind: ind == 0,
            "1": lambda out, ind: ind == 0,
        }
        inputs = self.get_input_ids
        outputs = self.get_output_ids
        if self.is_cyclic():
            return False
        for node in self.get_nodes:
            if not(node.id in inputs or node.id in outputs):
                if node.label in cond.keys():
                    if(not(cond[node.label](node.outdegree, node.indegree))):
                        return False
                else:
                    return False
        return True

    @classmethod
    def parse_parentheses(cls, *args):
        g = cls.empty()
        oper = ["&", "|", "~", "^", "0", "1", ""]
        inputDiv = {}
        for i, s in enumerate(args):
            o = g.add_node(f"o{i}")
            n = g.add_node(f"")
            g.add_edge(n, o)
            g.add_output_id(o)
            current_node = g.get_node_by_id(n)
            s2 = ""
            for char in s:
                if char == '(':
                    current_node.set_label(current_node.get_label + s2)
                    id = g.add_node('', {}, {})
                    g.add_edge(id, current_node.id)
                    current_node = g.get_node_by_id(id)
                    s2 = ""
                elif char == ')':
                    current_node.set_label(current_node.get_label + s2)
                    if current_node.label not in oper:
                        if current_node.label in inputDiv:
                            idDiv = inputDiv[current_node.label]
                            g.add_edge(idDiv, current_node.get_children_ids[0])
                            g.remove_node_by_id(current_node.id)
                            current_node = g.get_node_by_id(idDiv)
                        else:
                            idDiv = g.add_node("")
                            g.add_edge(
                                idDiv, current_node.get_children_ids[-1])
                            g.remove_edge(current_node.id,
                                          current_node.get_children_ids[-1])
                            g.add_edge(current_node.id, idDiv)
                            g.add_input_id(current_node.id)
                            inputDiv[current_node.label] = idDiv
                            current_node = g.get_node_by_id(idDiv)
                        pass
                    current_node = g.get_node_by_id(
                        current_node.get_children_ids[-1])
                    s2 = ""
                elif char in oper:
                    if current_node.label == char:
                        pass
                    else:
                        s2 += char
                else:
                    s2 += char
        return g

    @classmethod
    def from_table(cls, bits: str):
        nbVar = math.log2(len(bits))
        if not nbVar.is_integer():
            raise Exception("this table is not a boolean table")
        G = cls.empty()
        idsSplit = []
        for i in range(int(nbVar)):
            idSplit = G.add_node("")
            G.add_input_node(idSplit, label=f"I{i}")
            idsSplit.append(idSplit)

        outputid = G.add_node("|", {}, {})
        G.add_output_node(outputid)
        for line, bit in enumerate(bits):
            if bit == "1":
                idAnd = G.add_node("&")
                G.add_edge(idAnd, outputid)
                line = bin(line)[2:]
                line = "0" * (int(nbVar) - len(line)) + line
                for i, bitEntry in enumerate(line):
                    if(bitEntry == "1"):
                        G.add_edge(idsSplit[i], idAnd)
                    else:
                        idNon = G.add_node("~")
                        G.add_edge(idNon, idAnd)
                        G.add_edge(idsSplit[i], idNon)
        return G

    @classmethod
    def from_kmap(cls, bits: str):
        return cls.parse_parentheses(ut.K_map_prop(bits))

    @classmethod
    def random_bool_circ(cls, size: int, input: int, output: int):
        G = cls.random(size, 1, form="DAG")
        nodes = G.get_nodes
        for node in nodes:
            if node.get_children_ids == []:
                G.add_output_node(node.get_id)
            if node.get_parent_ids == []:
                G.add_input_node(node.get_id)
        isize = len(G.get_input_ids)
        osize = len(G.get_output_ids)
        if isize < input:
            for i in range(input-isize):
                G.add_input_node(randint(1, len(nodes)))
        if isize > input:
            pass
        if osize < output:
            for i in range(output-osize):
                G.add_output_node(randint(1, len(nodes)))
        if osize > output:
            pass

        for node in nodes:
            children = node.get_children_ids
            parents = node.get_parent_ids
            if len(parents) == 1 and len(children) == 1:
                node.set_label("~")
            elif len(parents) == 1 and len(children) > 1:
                node.set_label("")
            elif len(parents) > 1 and len(children) == 1:
                tab = ["&", "|", "^"]
                node.set_label(tab[randint(0, 2)])
            else:
                tab = ["&", "|", "^"]
                idg = G.add_node(tab[randint(0, 2)], {}, {})
                node.set_label("")
                G.add_edge(idg, node.get_id)
                for ch in parents:
                    G.add_edge(ch, idg)
                    G.remove_edge(node.get_id, ch)
        return G

    @classmethod
    def adder(cls, n: int):
        G = cls.empty()
        ba = G.add_node()
        bb = G.add_node()
        bc = G.add_node()
        G.add_input_node(ba, label="a0")
        G.add_input_node(bb, label="b0")
        G.add_input_node(bc, label="c")
        xor1 = G.add_node("^")
        xor2 = G.add_node("^")
        split = G.add_node("")
        and1 = G.add_node("&")
        and2 = G.add_node("&")
        or1 = G.add_node("|")
        G.add_output_node(xor2, label="r0")
        G.add_output_node(or1, label="c'")

        G.add_edges((ba, xor1), (ba, and1),
                    (bb, xor1), (bb, and1),
                    (bc, xor2), (bc, and2),
                    (xor1, split), (split, and2), (split, xor2),
                    (and1, or1), (and2, or1))
        for i in range(0, n - 1):
            add = G.copy()
            ia = len(add.get_input_ids) // 2
            ib = ia
            for node in add.get_input_ids:
                n = G.get_node_by_id(node)
                if n.get_label[0] == "a":
                    n.set_label(f"a{ia}")
                    ia += 1
                if n.get_label[0] == "b":
                    n.set_label(f"b{ib}")
                    ib += 1
            ir = len(add.get_output_ids) - 1
            outs = add.get_output_ids[::-1]
            for node in outs:
                n = G.get_node_by_id(node)
                if n.get_label[0] == "r":
                    n.set_label(f"r{ir}")
                    ir += 1
            rin = add.get_input_ids[-1]
            rin += G.max_id() + 1
            rout = G.get_output_ids[-1]
            G.iparallel(add)
            G.add_edge(G.get_node_by_id(rout).get_parent_ids[0],
                       G.get_node_by_id(rin).get_children_ids[0])
            G.remove_nodes_by_id(rin, rout)
        inputs = G.get_input_ids[:-1]
        G.set_input_ids(inputs[0::2] +
                        inputs[1::2] +
                        [G.get_input_ids[-1]])
        return G

    @classmethod
    def half_adder(cls, n: int):
        G = cls.adder(n)
        inlst = G.get_input_ids
        reg = inlst[-1]
        inlst.pop()
        G.set_input_ids(inlst)
        G.get_node_by_id(reg).set_label("0")
        return G

    @classmethod
    def int_to_bites(cls, i: int, n: int = 8):
        bites = bin(i)[2:]        
        if len(bites) > n:
            raise ValueError("The number is too big")
        bites = bin(i)[2:]
        bites = "0" * (int(n - len(bites))) + bites
        G = cls.empty()
        for b in bites:
            id = G.add_node(b)
            G.add_output_node(id)
        return G

    def copy_gate(self, id: int):
        node = self.get_node_by_id(id)
        if node.get_label != "1" and node.get_label != "0":
            raise ValueError(f"Invalid node {id}")
        idco = node.get_children_ids[0]
        copy = self.get_node_by_id(idco)
        if copy.get_label != '':
            raise ValueError(f"Invalid node {copy.get_id}")
        for child in copy.get_children_ids:
            n = self.add_node(node.get_label)
            if child in self.get_output_ids:
                self.add_output_node(n, label=self.get_node_by_id(child).get_label)
            self.add_edge(n, child)
        self.remove_nodes_by_id(id, idco)

    def and_gate(self, id: int):
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
            n = self.add_node("0")
            childet = et.get_children_ids[0]
            self.add_edge(n, childet)
            if et.get_children_ids[0] in self.get_output_ids:
                self.add_output_node(n, label=self.get_node_by_id(
                    et.get_children_ids[0]).get_label)
            self.remove_nodes_by_id(id, idet)
        if label == "1":
            self.remove_node_by_id(id)

    def or_gate(self, id: int):
        node = self.get_node_by_id(id)
        label = node.get_label
        if label != "1" and label != "0":
            raise ValueError(f"Invalid node {n.get_children_ids[0]}")
        idet = node.get_children_ids[0]
        ou = self.get_node_by_id(idet)
        if ou.get_label != '|':
            raise ValueError(f"Invalid node {ou.get_id}")
        if label == "1":
            for parent in ou.get_parent_ids:
                if parent != id:
                    n = self.add_node('')
                    self.add_edge(parent, n)
            n = self.add_node("1")
            childet = ou.get_children_ids[0]
            self.add_edge(n, childet)
            if ou.get_children_ids[0] in self.get_output_ids:
                self.add_output_node(n, label=self.get_node_by_id(
                    ou.get_children_ids[0]).get_label)
            self.remove_nodes_by_id(id, idet)
        if label == "0":
            self.remove_node_by_id(id)

    def not_gate(self, id) -> None:
        n = self.get_node_by_id(id)
        if(self.get_node_by_id(n.get_children_ids[0]).get_label != "~"):
            raise ValueError(f"Invalid node {n.get_children_ids[0]}")
        id_new = 0
        if(n.get_label == "0"):
            id_new = self.add_node("1")
        elif(n.get_label == "1"):
            id_new = self.add_node("0")
        else:
            raise ValueError(f"Invalid node {id}")
        not_next = self.get_node_by_id(
            n.get_children_ids[0]).get_children_ids[0]
        self.add_edge(id_new, not_next)
        if not_next in self.get_output_ids:
            self.add_output_node(
                id_new, label=self.get_node_by_id(not_next).get_label)
        self.remove_nodes_by_id(id, n.get_children_ids[0])

    def neutral_gate(self, id: int) -> None:
        n = self.get_node_by_id(id)
        if len(n.get_parent_ids) > 0:
            raise ValueError(f"Invalid node {id}")
        id_new = 0
        if (n.get_label == "|" or n.get_label == "^"):
            id_new = self.add_node("0")
        elif n.get_label == "&":
            id_new = self.add_node("1")
        else:
            raise ValueError(f"Invalid node {id}")
        node_next = n.get_children_ids[0]
        self.add_edge(id_new, node_next)
        if node_next in self.get_output_ids:
            self.add_output_node(
                id_new, label=self.get_node_by_id(node_next).get_label)
        self.remove_nodes_by_id(id)

    def xor_gate(self, id: int) -> None:
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

    def __switch_gate(self, id: int) -> None:
        node = self.get_node_by_id(id)
        if node.label == '&' or node.label == '|' or node.label == '^':
            self.neutral_gate(id)
        else:
            children = node.get_children_ids
            if len(children) != 1:
                raise ValueError("more than 1 child")
            label = self.get_node_by_id(children[0]).get_label
            if label == '':
                self.copy_gate(id)
            elif label == '&':
                self.and_gate(id)
            elif label == '|':
                self.or_gate(id)
            elif label == '~':
                self.not_gate(id)
            elif label == '^':
                self.xor_gate(id)

    def evaluate(self) -> None:
        change = True
        while change:
            change = False
            for id in self.get_node_ids:
                n = self.get_node_by_id(id)
                if n != None and len(n.get_parent_ids) == 0:
                    if len(n.get_children_ids) == 0:
                        self.remove_node_by_id(id)
                        continue
                    if ((n.get_label != "0" and n.get_label != "1") or
                       n.get_children_ids[0] not in self.get_output_ids):
                        self.__switch_gate(id)
                        change = True
