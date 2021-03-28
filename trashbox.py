import random
from random import randint


def mod_exp(a, b, n):
    # Выход из рекурсии при возведении a в степень 0
    if b == 0:
        return 1  # Взятие модуля n от a в степень 0
    # Проверка четности степени
    if b % 2 == 0:
        # Получение остатка для a в степень в двое меньше b
        x = mod_exp(a, b / 2, n)
        return x * x % n  # Получение остатка для a в степень b

    # Получение остатка для a в степень в двое меньше b
    x = mod_exp(a, (b - 1) / 2, n)
    x = x * x % n
    return a * x % n  # Получение остатка для a в степень b


def decrypt_rsa(c, d, p, q, n):
    d1 = d % (p - 1)  # Получение остатка от деления показателя d на p-1
    d2 = d % (q - 1)  # Получение остатка от деления показателя d на q-1

    # Использование метода повторного возведения в квадрат для высичления
    m1 = mod_exp(c, d1, p)  # с^d1 mod p
    m2 = mod_exp(c, d2, q)  # с^d2 mod q

    # Получение обратного элемента мультипликативной группы вычитов (q^(-1))
    t, x, y = extended_euclid(q, p)
    r = x % p

    # Формула китайской теоремы об остатках
    m = (((m1 - m2) * r) % p) * q + m2

    return m;


def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def euclid(a, b):
    t = 0
    while b > 0:
        t = b
        b = a % b
        a = t
    return a


def rabin_miller(n, r):
    b = n - 1
    k = -1
    beta = []

    # Получение двоичное записи числа b
    k = k + 1
    beta.append(b % 2)
    b = b // 2
    while b > 0:
        k = k + 1
        beta.append(b % 2)
        b = b // 2

    # Повторяем метод Рабина-Миллера r раз
    for j in range(r):
        a = randint(2, n - 1)  # Получаем случайное основание a
        # Проверяем взаимную простоту a и n
        if euclid(a, n) > 1:
            return False
        # Возведение числа a в степень n-1
        # с помощью метода повторного возведения
        # в квадрат с использованием рекуррентного соотношения
        # и проверки на нетривиальный корень из 1
        d = 1
        for i in range(k, -1, -1):
            x = d
            d = d * d % n  # Получение остатка от деления на n
            # Проверка на нетривиальный корень из 1
            if d == 1 and x != 1 and x != n - 1:
                return False
            # Рекуррентное соотношение
            if beta[i] == 1:
                d = d * a % n
        # Если НОД(a,n) не равен 1
        if d != 1:
            return False  # n - составное
    return True


def eratosphen(n):
    a = []

    # Получение списка заполненного 1
    for j in range(n + 1):
        a.append(1)

    j = 2
    # Просматриваем все числа меньше n
    while j * j <= n:
        # Если число не вычеркнуто, то оно - простое
        if a[j] == 1:
            i = j * j
            # Вычеркиваются все числа кратные j
            while i <= n:
                a[i] = 0
                i = i + j
        j = j + 1

    p = []

    # Получаем список простых чисел
    for j in range(2, n + 1):
        if a[j] == 1:
            p.append(j)

    return p


def is_prime(n):
    p = eratosphen(810)  # Получение первых 150 простых чисел
    m = len(p)

    # Сравнение сгенерированного числа n с первыми 150 простыми числами
    for i in range(m):
        # Проверка делится ли число n на одно из первых простых чисел
        if n % p[i] == 0:
            # Если сгенерированное число n является одним
            # из первых простых чисел,
            if n == p[i]:
                return True  # то n - простое
            else:
                return False  # иначе n - составное

    r = 60  # Количество повторение теста Рабина-Миллера
    return rabin_miller(n, r)


def generate_prime(N):
    m = N // 2  # Генерация случайного числа
    n = randint(2, m)  # из интервала 2..N/2
    n = 2 * n - 1  # Получение нечетного случайного числа

    # Пока число не простое, продолжаем генерировать
    while is_prime(n) != True:
        m = N // 2  # Генерация случайного числа
        n = randint(2, m)  # из интервала 2..N/2
        n = 2 * n - 1  # Получение нечетного случайного числа
    return n


def extended_euclid(a, b):
    x1 = 0
    x = 1
    y1 = 1
    y = 0

    # Пока делитель не равен 0
    while b > 0:
        q = a // b  # находим целую часть от деления a на b

        t = b
        b = a % b  # находим остаток от деления a на b
        a = t

        # находим коэффициент x в линейной комбинации a и b
        t = x1
        x1 = x - (q * x1)
        x = t

        # находим коэффициент y в линейной комбинации a и b
        t = y1
        y1 = y - (q * y1)
        y = t
    return a, x, y


def generateKeys_rsa(N, e):
    p = generate_prime(N)  # Генерация простого числа p
    q = generate_prime(N)  # Генерация простого числа q
    f = (p - 1) * (q - 1)  # Вычисление функции Эйлера
    t, x, y = extended_euclid(e, f)  # Находим НОД(e,f)

    # Генерируем простые числа p и q, пока они равны или НОД(e,f) не равен 1
    while p == q or t > 1:
        p = generate_prime(N)  # Генерация простого числа p
        q = generate_prime(N)  # Генерация простого числа q
        f = (p - 1) * (q - 1)  # Вычисление функции Эйлера
        t, x, y = extended_euclid(e, f)  # Находим НОД(e,f)

    n = p * q  # Вычисление криптомодуля
    d = x % f  # Вычисление числа d
    return d, n, p, q


def action_1():
    print('Введите e (нечетное, от 1 до 65 535)')
    eKey = input()
    if isint(eKey):
        eKey = int(eKey)
        if eKey < 1 or eKey > 65535 or eKey % 2 == 0:
            print('Число e введено неверно! Введите нечетное число, от 1 до 65535')
            action_1()
        else:
            N = 2000000000
            d_key, nKey, p, q = generateKeys_rsa(N, eKey)
            print('Открытый ключ: ' + str(eKey) + ', ' + str(nKey))
            print('Закрытый ключ: ' + str(d_key) + ', ' + str(nKey))
            print('Простое число p: ' + str(p))
            print('Простое число q ' + str(q))
    else:
        print('Число e введено неверно! Введите нечетное число, от 1 до 65535')
        action_1()


def action_2():
    print('Введите первую часть открытого ключа (e)')
    eKey = input()
    print('Введите вторую часть открытого ключа (n)')
    nKey = input()
    print('Введите сообщение, которое хотите зашифровать')
    message = input()
    if isint(eKey) and isint(nKey) and isint(message):
        result = mod_exp(int(message), int(eKey), int(nKey))
        print('Зашифрованное сообщение')
        print(str(result))
    else:
        print('Введенные данные некорректны')
        action_2()


def action_3():
    print('Введите первую часть закрытого ключа (d)')
    d_key = input()
    print('Введите вторую часть закрытого ключа (n)')
    nKey = input()
    print('Введите сообщение, которое хотите расшифровать')
    message = input()
    print('Введите простое число p')
    p = input()
    print('Введите простое число q')
    q = input()
    if isint(d_key) and isint(nKey) and isint(message) and isint(p) and isint(q):
        result = 0
        result = decrypt_rsa(int(message), int(d_key), int(p), int(q), int(nKey))
        print('Расшифрованное сообщение')
        print(str(result))
    else:
        print('Введенные данные некорректны')
        action_3()


def start():
    while True:
        print('Сгенерировать ключи - 1')
        print('Зашифровать сообщение - 2')
        print('Расшифровать сообщение - 3')
        action = input()
        if isint(action):
            if int(action) == 1:
                action_1()
            elif int(action) == 2:
                action_2()
            elif int(action) == 3:
                action_3()
        else:
            print('Такой команды нет')



if __name__ == '__main__':
    start()
