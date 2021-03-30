import math, random


def Euclid(a, b):
    """Алгоритм Евклида для нахождения НОД"""
    if b == 0:
        return a
    return Euclid(b, a % b)


def RabinMiller(n, r):
    """Тест Рабина-Миллера для проверки простоты числа"""
    b = n - 1

    beta = [b % 2]
    b = math.floor(b / 2)
    while b > 0:
        beta.append(b % 2)
        b = math.floor(b / 2)

    for i in range(r):
        a = random.randint(2, n - 1)
        if Euclid(a, n) > 1:
            return False
        d = 1
        for j in range(len(beta) - 1, -1, -1):
            x = d
            d = (d * d) % n
            if (d == 1) and (x != 1) and (x != n - 1):
                return False
            if beta[j] == 1:
                d = (d * a) % n
        if d != 1:
            return False
    return True


i = 99999999977

print(RabinMiller(i, 150))
