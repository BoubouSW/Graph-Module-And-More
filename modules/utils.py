import math
from tokenize import String

from zmq import XPUB_VERBOSE


def gray_code(n: int):
    """Genereta a gray code of length n
    rec function:
    if n == "0":
        return [""]
    resL = []
    resR = []
    for i in gray_code(n-1):
        resL += ["0" + i]
        resR += ["1" + i]
    return resL + list(reversed(resR))
    """
    res = [""]
    for _ in range(n):
        res = ["0" + x for x in res] + ["1" + x for x in reversed(res)]
    return res


def K_map(bits: str):
    """Generate a K map of a given bits string"""
    nbVar = math.log2(len(bits))
    if not nbVar.is_integer():
        raise Exception("this table is not a boolean table")
    nbVar = int(nbVar)
    gcode_lig = gray_code(nbVar // 2)
    gcode_col = gray_code(nbVar - nbVar // 2)
    k_map = []
    for lig in gcode_lig:
        k_line = []
        for col in gcode_col:
            k_line.append(bits[int(lig + col, 2)])
        k_map.append(k_line)
    return k_map


def test_box(tab, x, y, w, h):
    """Test if a box conteint a 0"""
    cross_one = False
    for j in range(x, x + w):
        for i in range(y, y + h):
            if tab[i % len(tab)][j % len(tab[0])] == "0":
                return False
            elif tab[i % len(tab)][j % len(tab[0])] == "1":
                cross_one = True
    if cross_one:
        for j in range(x, x + w):
            for i in range(y, y + h):
                tab[i % len(tab)][j % len(tab[0])] = 2
    return cross_one


def trans_box(x: int, y: int, w: int, h: int, gcode_lig, gcode_col) -> String:
    forme = "|("
    nb_col = len(gcode_col[0])
    col_var = {i + nb_col: gcode_col[x][i]
               for i in range(0, len(gcode_col[0]))}
    for i in range(x + 1, x + w):
        for s, b in enumerate(gcode_col[i]):
            if(s+nb_col in col_var and col_var[s + nb_col] != b):
                del col_var[s + nb_col]

    lig_var = {i: gcode_lig[y][i] for i in range(0, len(gcode_lig[0]))}
    for i in range(y, y + h):
        for s, b in enumerate(gcode_lig[i]):
            if(s in lig_var and lig_var[s] != b):
                del lig_var[s]
    for x in lig_var:
        op = ""
        if lig_var[x] == "0":
            op = "~"
        forme += op + "(x" + str(x) + ")" + "&"
    for x in col_var:
        op = ""
        if col_var[x] == "0":
            op = "~"
        forme += op + "(x" + str(x) + ")" + "&"
    forme = forme[:-1] + ")"
    return forme


def K_map_prop(bits: str) -> String:
    k_map = K_map(bits)
    nbVar = int(math.log2(len(bits)))

    gcode_lig = gray_code(nbVar // 2)
    gcode_col = gray_code(nbVar - nbVar // 2)

    def test_end():
        for l in k_map:
            if "1" in l:
                return False
        return True

    formule = ""
    i = int(nbVar)
    while i >= 0:
        for j in range(i, -1, -1):
            h_size = 2 ** (i - j)
            w_size = 2 ** j
            if h_size > len(k_map) or w_size > len(k_map[0]):
                continue

            y_step = h_size if h_size == len(k_map) else 1
            x_step = w_size if w_size == len(k_map[0]) else 1
            for y in range(0, len(k_map), y_step):
                for x in range(0, len(k_map[0]), x_step):
                    if test_box(k_map, x, y, w_size, h_size):
                        formule += trans_box(x, y, w_size,
                                             h_size, gcode_lig, gcode_col)
                        if(test_end()):
                            return formule[1:]

        i -= 1
    return ""
