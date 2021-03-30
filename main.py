import random
import math

m = 810


def Eratosphen(n):
    """Генерирует решето Эратосфена"""
    sieve = list(range(n + 1))
    sieve[1] = 0  # без этой строки итоговый список будет содержать единицу
    for i in sieve:
        if i > 1:
            for j in range(i + i, len(sieve), i):
                sieve[j] = 0
    return sieve


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


def IsPrime(n):
    """Тест на проверку простоты числа с помощью решета Эратосфена, иначе тест Рабина-Миллера"""
    # P = Eratosphen(m)
    #
    # for j in range(len(P)):
    #     if (n % P[j]) == 0:
    #         if n == P[j]:
    #             return True
    #         else:
    #             return False
    r = 150  # Количество повторений теста Рабина-Миллера
    return RabinMiller(n, r)


def GeneratePrime(N):
    """Генерация простого числа"""
    n = random.randint(2, math.floor(N / 2))
    n = 2 * n - 1
    while not IsPrime(n):
        n = random.randint(2, math.floor(N / 2))
        n = 2 * n - 1
    return n


def ExtendedEuclid(a, b):
    """Расширенный алгоритм Евклида для нахождения НОД"""
    if not b:
        return 1, 0, a
    y, x, g = ExtendedEuclid(b, a % b)
    return x, y - math.floor(a / b) * x, g


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
    x, y, t = ExtendedEuclid(e, f)
    while t > 1:
        e = e + 2
        x, y, t = ExtendedEuclid(e, f)

    n = p * q
    d = x % f
    return d, n, p, q, e


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


def DecryptRSA(c, d, p, q, n):
    """Расшифровка шифртекста"""
    d1 = d % (p - 1)  # Получение остатка от деления показателя d на p-1
    d2 = d % (q - 1)  # Получение остатка от деления показателя d на q-1

    # Использование метода повторного возведения в квадрат для высичления
    m1 = ModExp(c, d1, p)  # с^d1 mod p
    m2 = ModExp(c, d2, q)  # с^d2 mod q

    # Получение обратного элемента мультипликативной группы вычитов (q^(-1))
    x, y, t = ExtendedEuclid(q, p)
    r = x % p

    # Формула китайской теоремы об остатках
    m = (((m1 - m2) * r) % p) * q + m2

    return m


def step1():
    N = 10 ** 20
    d, n, p, q, e = GenerateKeyRSA(N)
    print('Открытый ключ (e, n): ' + str(e) + ', ' + str(n))
    print('Закрытый ключ (d, n): ' + str(d) + ', ' + str(n))
    print('Простое число p: ' + str(p))
    print('Простое число q: ' + str(q))


def step2():
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
    try:
        print('Введите первую часть закрытого ключа (d)')
        d = int(input())
        print('Введите вторую часть закрытого ключа (n)')
        n = int(input())
        print('Введите сообщение, которое хотите расшифровать')
        message = int(input())
        print('Введите простое число p')
        p = int(input())
        print('Введите простое число q')
        q = int(input())
    except ValueError:
        print('Введенные данные некорректны')
        step3()

    result = DecryptRSA(message, d, p, q, n)
    print('Расшифрованное сообщение')
    print(str(result))


def start():
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
