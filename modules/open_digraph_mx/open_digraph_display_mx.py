import os

class open_digraph_display_mx:
    def __str__(self) -> str:
        str_ret = f"I = {self.inputs}\n"
        for node in self.nodes.values():
            if not (node.get_id in self.inputs or node.get_id in self.outputs):
                str_ret += str(node)
        str_ret += f"O = {self.outputs}\n"
        return str_ret

    def __repr__(self) -> str:
        return str(self)

    def save_as_dot_file(self, path: str = "mygraph", verbose: bool = False) -> None:
        """
        La fonction génère un fichier .dot qu'on peut ensuite
        visualiser à l'aide de divers outils
        (en l'occurence on utilise l'extension "Graphviz" sur vscode)
        """
        ipt = self.get_input_ids
        opt = self.get_output_ids
        with open(f"{path}.dot", "w") as file:
            file.write("digraph{")
            for node in self.get_nodes:
                if verbose:
                    label = f"{node.get_label}\\n{node.get_id}"
                else:
                    label = f"{node.get_label}"
                if node.get_id in ipt:
                    color = "red"
                elif node.get_id in opt:
                    color = "green"
                else:
                    color = "black"
                file.write(
                    f"{node.get_id}[id={node.get_id},label=\"{label}\",color={color}];")
                for child in node.get_children_ids:
                    for _ in range(node.get_children_id_mult(child)):
                        file.write(f"{node.get_id}->{child};")

            file.write("}")

    def display(self, name: str = "mygraph"):
        self.save_as_dot_file(name)
        os.system(f"dot -Tpdf {name}.dot -o {name}.pdf")
        #os.system(f"brave {name}.pdf")
        os.remove(f"{name}.dot")
