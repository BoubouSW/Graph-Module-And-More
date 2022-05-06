import math
from random import randint
import modules.utils as ut


class Bool_circ_construct_mx:

    @classmethod
    def parse_parentheses(cls,*args:str):
        """
        creer bool_circ à partir de formule propositionnelle 
        """
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
        """
        creer bool_circ à partir table de verite
        """
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
        """
        creer un bool_circ à partir d'une kmap
        """
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
        """
        creer bool_circ à partir d'un int (creer adder)
        """
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
        for i, o in enumerate(G.get_output_ids[0:-1]):
            n = G.get_node_by_id(o)
            n.set_label(f"r{i}")
        return G

    @classmethod
    def half_adder(cls, n: int):
        """
        creer bool_circ à partir d'un int (creer demi-adder)
        """
        G = cls.adder(n)
        inlst = G.get_input_ids
        reg = inlst[-1]
        inlst.pop()
        G.set_input_ids(inlst)
        G.get_node_by_id(reg).set_label("0")
        return G

    @classmethod
    def int_to_binary(cls, i: int, n: int = 8):
        """
        creer un bool_circ à partir d'un entier et du nb de bits pour encoder
        """
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
    
    @classmethod
    def hamming_enc(cls):
        """
        creer encodeur hamming
        """
        return cls.parse_parentheses("(x0)^(x1)^(x3)", "(x0)^(x2)^(x3)",
                                     "(x0)", "(x1)^(x2)^(x3)", "(x1)",
                                     "(x2)", "(x3)")

    @classmethod
    def hamming_dec(cls):
        """
        creer decodeur hamming
        """
        top: Bool_circ = cls.parse_parentheses("(x0)^(x2)^(x4)^(x6)", "(x1)^(x2)^(x5)^(x6)",
                                               "(x2)", "(x3)^(x4)^(x5)^(x6)", "(x4)",
                                               "(x5)", "(x6)")
        bottom: Bool_circ = cls.parse_parentheses("((x0)&(x1)&(~(x3)))^(x2)",
                                                  "((x0)&(~(x1))&(x3))^(x4)",
                                                  "((~(x0))&(x1)&(x3))^(x5)", "((x0)&(x1)&(x3))^(x6)")
        top.icompose(bottom)
        return top
