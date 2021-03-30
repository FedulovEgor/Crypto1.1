import math


def ModExp(a, b, n):
    """Возведение в степень по модулю"""
    beta = [b % 2]
    b = math.floor(b / 2)
    while b > 0:
        beta.append(b % 2)
        b = math.floor(b / 2)

    d = 1
    for i in range(len(beta) - 1, -1, -1):
        d = (d * d) % n
        if beta[i] == 1:
            d = (d * a) % n
    return d


print(ModExp(4, 13, 497))
