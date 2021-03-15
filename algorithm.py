import random

m = 149  # ограничение проходов или что-то в этом духе из методички Воронова


# получить P - решето Эратосфена, проверить на итераторы
def Eratosphen(n):
    A = [0]
    for j in range(1, n):
        A.append(1)
    j = 1
    while (j ** 2) < n:
        if A[j] == 1:
            i = j ** 2
            while i < n:
                A[i] = 0
                i += j
        j += 1
    m_my = 0
    P = [0]
    for j in range(1, n):
        if A[j] == 1:
            P.append(0)
            m_my += 1
            P[m] = j
    return P


def RabinMiller(n, r):
    pass


def IsPrime(n):
    # использует массив простых чисел P[1..m]
    P = Eratosphen(m)
    for j in range(0, m):
        if (n % P[j]) == 0:
            if n == P[j]:
                return True
            else:
                return False
    r = 1  # ?????????????????????????????? из методички Воронова не понял че тут
    return RabinMiller(n, r)


def GeneratePrime(nBig):
    n = random.randint(2, nBig / 2)  # где деление - округлить результат деления до нижнего целого
    n = 2 * n - 1
    while not IsPrime(n):
        n = random.randint(2, nBig / 2)  # где деление - округлить результат деления до нижнего целого
        n = 2 * n - 1
    return n


def ExtendedEuclid(a, b):
    if b == 0:
        return [a, 1, 0]
    d, xx, yy = ExtendedEuclid(b, a % b)  # d - d, xx - x', yy - y'
    # хз, будет ли так работать, то что выше
    # проверил, да, будет работать
    x = yy
    y = xx - (a / b) * yy  # где деление - округлить результат деления до нижнего целого
    return [d, x, y]


def GenerateKeyRSA(nBig):
    p = GeneratePrime(nBig)
    q = GeneratePrime(nBig)
    while p == q:
        p = GeneratePrime(nBig)
        q = GeneratePrime(nBig)
    f = (p - 1) * (q - 1)
    e = 1
    e += 2
    t, x, y = ExtendedEuclid(e, f)
    # да, это тоже работает, то что выше
    while t > 1:
        e += 2
        t, x, y = ExtendedEuclid(e, f)
    n = p * q
    d = x % f
    return [e, d, n]
