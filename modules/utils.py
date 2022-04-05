import math


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
    for i in range(x, x + w):
        for j in range(y, y + h):
            if tab[i % len(tab)][j % len(tab[0])] == "0":
                return False
    return True


def K_map_prop(bits: str):
    k_map = K_map(bits)
    nbVar = math.log2(len(bits))

    def test_end():
        for l in k_map:
            if 1 in l:
                return False
        return True

    i = int(nbVar)
    while test_end() and i >= 0:
        for j in range(i, -1, -1):
            h_size = 2 ** (i - j)
            w_size = 2 ** j
            if h_size > len(k_map) or w_size > len(k_map[0]):
                continue

            y_step = h_size if h_size == len(k_map) else 1
            x_step = w_size if w_size == len(k_map[0]) else 1
            for y in range(0, len(k_map), y_step):
                for x in range(0, len(k_map[0]), x_step):
                    test_box(k_map, x, y, w_size, h_size)

        i -= 1
