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
