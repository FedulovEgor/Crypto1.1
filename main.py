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
    k = -1
    beta = []

    # k += 1
    beta.append(b % 2)
    b = math.floor(b / 2)

    while b > 0:
        # k += 1
        beta.append(b % 2)
        b = math.floor(b / 2)

    for j in range(r):
        a = random.randint(2, n - 1)
        if Euclid(a, n) > 1:
            return False
        d = 1
        for i in range(len(beta) - 1, 0, -1):
            x = d
            d = (d ** 2) % n
            if (d == 1) and (x != 1) and (x != n - 1):
                return False
            if beta[i] == 1:
                d = (d * a) % n
        if d != 1:
            return False
    return True
    # if n == 2:
    #     return True
    #
    # if n % 2 == 0:
    #     return False
    #
    # k, s = 0, n - 1
    # while s % 2 == 0:
    #     k += 1
    #     s //= 2
    # for _ in range(r):
    #     a = random.randrange(2, n - 1)
    #     x = pow(a, s, n)
    #     if x == 1 or x == n - 1:
    #         continue
    #     for _ in range(k - 1):
    #         x = pow(x, 2, n)
    #         if x == n - 1:
    #             break
    #     else:
    #         return False
    # return True


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
    # Выход из рекурсии при возведении a в степень 0
    if b == 0:
        return 1  # Взятие модуля n от a в степень 0
    # Проверка четности степени
    if b % 2 == 0:
        # Получение остатка для a в степень в двое меньше b
        x = ModExp(a, b / 2, n)
        return x * x % n  # Получение остатка для a в степень b

    # Получение остатка для a в степень в двое меньше b
    x = ModExp(a, (b - 1) / 2, n)
    x = x * x % n
    return a * x % n  # Получение остатка для a в степень b


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
    N = 10**20
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
