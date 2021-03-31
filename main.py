import random
import math


def Eratosphen(n):
    """Генерирует решето Эратосфена"""
    a = []

    for j in range(n + 1):
        a.append(1)

    j = 2
    while j * j <= n:
        if a[j] == 1:
            i = j * j
            while i <= n:
                a[i] = 0
                i = i + j
        j = j + 1

    p = []

    for j in range(2, n + 1):
        if a[j] == 1:
            p.append(j)

    return p


def Euclid(a, b):
    """Алгоритм Евклида для нахождения НОД"""
    if b == 0:
        return a
    return Euclid(b, a % b)


def RabinMiller(n, r):
    """Тест Рабина-Миллера для проверки простоты числа"""
    b = n - 1

    beta = [b % 2]
    b = b // 2
    while b > 0:
        beta.append(b % 2)
        b = b // 2

    for j in range(r):
        a = random.randint(2, n - 1)
        if Euclid(a, n) > 1:
            return False
        d = 1
        for i in range(len(beta) - 1, -1, -1):
            x = d
            d = d * d % n
            if d == 1 and x != 1 and x != n - 1:
                return False
            if beta[i] == 1:
                d = d * a % n
        if d != 1:
            return False
    return True


def IsPrime(n):
    """Тест на проверку простоты числа с помощью решета Эратосфена, иначе тест Рабина-Миллера"""
    p = Eratosphen(810)

    for i in range(len(p)):
        if n % p[i] == 0:
            if n == p[i]:
                return True
            else:
                return False

    r = 60
    return RabinMiller(n, r)


def GeneratePrime(N):
    """Генерация простого числа"""
    m = N // 2
    n = random.randint(2, m)
    n = 2 * n - 1

    while not IsPrime(n):
        m = N // 2
        n = random.randint(2, m)
        n = 2 * n - 1
    return n


def ExtendedEuclid(a, b):
    """Расширенный алгоритм Евклида для нахождения НОД и линейной комбинации"""
    if not b:
        return a, 1, 0
    d, xx, yy = ExtendedEuclid(b, a % b)
    x = int(yy)
    y = int(xx - a // b * yy)
    return d, x, y


def GenerateKeyRSA(N):
    """Генерация ключей RSA"""
    p = GeneratePrime(N)
    q = GeneratePrime(N)
    while p == q:
        p = GeneratePrime(N)
        q = GeneratePrime(N)

    f = (p - 1) * (q - 1)
    e = 1

    e = e + 2
    t, x, y = ExtendedEuclid(e, f)
    while t > 1:
        e = e + 2
        t, x, y = ExtendedEuclid(e, f)

    n = p * q
    d = x % f
    return e, d, n


def ModExp(a, b, n):
    """Возведение в степень по модулю"""
    beta = [b % 2]
    b = b // 2
    while b > 0:
        beta.append(b % 2)
        b = b // 2

    d = 1
    for i in range(len(beta) - 1, -1, -1):
        d = (d * d) % n
        if beta[i] == 1:
            d = (d * a) % n
    return d


def step1():
    """Генерация ключей"""
    # TODO: при большом N прога не абонент
    N = 109417386415705274218097073220403576120037329454492059909138421314763499842889347847179972578912673324976257528997818337970765372440271467435315933543338974563728164539274563715647292635473920374657489365648392736457483
    e, d, n = GenerateKeyRSA(N)
    print('Открытый ключ (e, n): ' + str(e) + ', ' + str(n))
    print('Закрытый ключ (d, n): ' + str(d) + ', ' + str(n))


def step2():
    """Шифрование сообщения"""
    try:
        print('Введите первую часть открытого ключа (e)')
        e = int(input())
        print('Введите вторую часть открытого ключа (n)')
        n = int(input())
        print('Введите сообщение, которое хотите зашифровать')
        message = int(input())
    except ValueError:
        print('Введенные данные некорректны')
        step2()

    result = ModExp(message, e, n)
    print('Зашифрованное сообщение')
    print(str(result))


def step3():
    """Дешифрование сообщения"""
    try:
        print('Введите первую часть закрытого ключа (d)')
        d = int(input())
        print('Введите вторую часть закрытого ключа (n)')
        n = int(input())
        print('Введите сообщение, которое хотите расшифровать')
        message = int(input())
    except ValueError:
        print('Введенные данные некорректны')
        step3()

    result = ModExp(message, d, n)
    print('Расшифрованное сообщение')
    print(str(result))


def start():
    """Начало работы"""
    while True:
        print('Сгенерировать ключи - 1')
        print('Зашифровать сообщение - 2')
        print('Расшифровать сообщение - 3')
        action = int(input())
        if action == 1:
            step1()
        elif action == 2:
            step2()
        elif action == 3:
            step3()
        elif action == 0:
            exit()
        else:
            print('Такой команды нет')
            start()


if __name__ == "__main__":
    start()
