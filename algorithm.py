import random
import math

m = 810


# получить P - решето Эратосфена, проверить на итераторы
def Eratosphen(n):
    A = []

    # Получение списка заполненного 1
    for j in range(n + 1):
        A.append(1)

    j = 2
    # Просматриваем все числа меньше n
    while j * j <= n:
        # Если число не вычеркнуто, то оно - простое
        if A[j] == 1:
            i = j * j
            # Вычеркиваются все числа кратные j
            while i <= n:
                A[i] = 0
                i = i + j
        j = j + 1

    p = []

    # Получаем список простых чисел
    for j in range(2, n + 1):
        if A[j] == 1:
            p.append(j)

    return p


def Euclid(a, b):
    if b == 0:
        return a
    return Euclid(b, a % b)


def RabinMiller(n, r):
    b = n - 1
    k = -1

    beta = []
    k += 1
    beta.append(b % 2)
    b = math.floor(b / 2)
    while b > 0:
        k += 1
        beta.append(b % 2)
        b = math.floor(b / 2)

    for j in range(r):
        a = random.randint(2, n - 1)
        if Euclid(a, n) > 1:
            return False
        d = 1
        for i in range(k, -1, -1):
            x = d
            d = (d ** 2) % n
            if (d == 1) and (x != 1) and (x != n - 1):
                return False
            if beta[i] == 1:
                d = (d * a) % n
        if d != 1:
            return False
    return True


def IsPrime(n):
    P = Eratosphen(m)

    for j in range(len(P)):
        if (n % P[j]) == 0:
            if n == P[j]:
                return True
            else:
                return False
    r = 150  # Количество повторений теста Рабина-Миллера
    return RabinMiller(n, r)


def GeneratePrime(nBig):
    n = random.randint(2, nBig // 2)
    n = 2 * n - 1
    while not IsPrime(n):
        n = random.randint(2, nBig // 2)
        n = 2 * n - 1
    return n


def ExtendedEuclid(a, b):
    if b == 0:
        return a, 1, 0
    d, xx, yy = ExtendedEuclid(b, a % b)
    x = yy
    y = xx - (a / b) * yy
    return int(d), int(x), int(y)


def GenerateKeyRSA(nBig, eKey):
    p = GeneratePrime(nBig)  # Генерация простого числа p
    q = GeneratePrime(nBig)  # Генерация простого числа q
    f = (p - 1) * (q - 1)
    t, x, y = ExtendedEuclid(eKey, f)
    # Генерируем простые числа p и q, пока они равны или НОД(e,f) не равен 1
    while p == q or t > 1:
        p = GeneratePrime(nBig)  # Генерация простого числа p
        q = GeneratePrime(nBig)  # Генерация простого числа q
        f = (p - 1) * (q - 1)  # Вычисление функции Эйлера
        t, x, y = ExtendedEuclid(eKey, f)  # Находим НОД(e,f)

    n = p * q  # Вычисление криптомодуля
    d = x % f  # Вычисление числа d
    return d, n, p, q


def ModExp(a, b, n):
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
    d1 = d % (p - 1)  # Получение остатка от деления показателя d на p-1
    d2 = d % (q - 1)  # Получение остатка от деления показателя d на q-1

    # Использование метода повторного возведения в квадрат для высичления
    m1 = ModExp(c, d1, p)  # с^d1 mod p
    m2 = ModExp(c, d2, q)  # с^d2 mod q

    # Получение обратного элемента мультипликативной группы вычитов (q^(-1))
    t, x, y = ExtendedEuclid(q, p)
    r = x % p

    # Формула китайской теоремы об остатках
    m = (((m1 - m2) * r) % p) * q + m2

    return m


def step1():
    print('Введите e нечетное, от 1 до 65 535')

    try:
        eKey = int(input())
    except ValueError:
        print('Число e введено неверно! Введите нечетное число, от 1 до 65535')
        step1()

    if eKey < 1 or eKey > 65535 or eKey % 2 == 0:
        print('Число e введено неверно! Введите нечетное число, от 1 до 65535')
        step1()
    else:
        N = 2000000000
        d_key, nKey, p, q = GenerateKeyRSA(N, eKey)
        print('Открытый ключ: ' + str(eKey) + ', ' + str(nKey))
        print('Закрытый ключ: ' + str(d_key) + ', ' + str(nKey))
        print('Простое число p: ' + str(p))
        print('Простое число q ' + str(q))


def step2():
    try:
        print('Введите первую часть открытого ключа (e)')
        eKey = int(input())
        print('Введите вторую часть открытого ключа (n)')
        nKey = int(input())
        print('Введите сообщение, которое хотите зашифровать')
        message = int(input())
    except ValueError:
        print('Введенные данные некорректны')
        step2()

    result = ModExp(message, eKey, nKey)
    print('Зашифрованное сообщение')
    print(str(result))


def step3():
    try:
        print('Введите первую часть закрытого ключа (d)')
        d_key = int(input())
        print('Введите вторую часть закрытого ключа (n)')
        nKey = int(input())
        print('Введите сообщение, которое хотите расшифровать')
        message = int(input())
        print('Введите простое число p')
        p = int(input())
        print('Введите простое число q')
        q = int(input())
    except ValueError:
        print('Введенные данные некорректны')
        step3()

    result = DecryptRSA(message, d_key, p, q, nKey)
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


start()
