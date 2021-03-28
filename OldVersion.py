import random, math


def ExtendedEuclid(a, b):
    """Расширенный алгоритм Евклида для нахождения НОД"""
    if not b:
        return 1, 0, a
    y, x, g = ExtendedEuclid(b, a % b)
    return x, y - (a // b) * x, g


print(ExtendedEuclid(336, 90))
