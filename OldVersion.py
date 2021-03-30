import random, math


def ExtendedEuclid(a, b):
    """Расширенный алгоритм Евклида для нахождения НОД"""
    if not b:
        return a, 1, 0
    d, xx, yy = ExtendedEuclid(b, a % b)
    x = yy
    y = xx - (math.floor(a / b)) * yy
    return d, x, y


print(ExtendedEuclid(336, 90))
