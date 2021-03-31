import random


def Eratosphen(n):
    """Генерирует решето Эратосфена"""
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


def Euclid(a, b):
    """Алгоритм Евклида для нахождения НОД"""
    if b == 0:
        return a
    return Euclid(b, a % b)


def RabinMiller(n, r):
    """Тест Рабина-Миллера для проверки простоты числа"""
    b = n - 1

    # Получение двоичное записи числа b
    beta = [b % 2]
    b = b // 2
    while b > 0:
        beta.append(b % 2)
        b = b // 2

    # Повторяем метод Рабина-Миллера r раз
    for j in range(r):
        a = random.randint(2, n - 1)  # Получаем случайное основание a
        # Проверяем взаимную простоту a и n
        if Euclid(a, n) > 1:
            return False
        # Возведение числа a в степень n-1 с помощью метода повторного возведения
        # в квадрат с использованием рекуррентного соотношения и проверки на нетривиальный корень из 1
        d = 1
        for i in range(len(beta) - 1, -1, -1):
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


def IsPrime(n):
    """Тест на проверку простоты числа с помощью решета Эратосфена, иначе тест Рабина-Миллера"""
    p = Eratosphen(810)

    # Сравнение сгенерированного числа n с первыми 150 простыми числами
    for i in range(len(p)):
        # Проверка делится ли число n на одно из первых простых чисел
        if n % p[i] == 0:
            # Если сгенерированное число n является одним из первых простых чисел,
            if n == p[i]:
                return True  # то n - простое
            else:
                return False  # иначе n - составное

    r = 63  # Количество повторений теста Рабина-Миллера
    return RabinMiller(n, r)


def GeneratePrime(N):
    """Генерация простого числа"""
    m = N // 2  # Генерация случайного числа
    n = random.randint(2, m)  # из интервала 2..N/2
    n = 2 * n - 1  # Получение нечетного случайного числа

    # Пока число не простое, продолжаем генерировать
    while not IsPrime(n):
        m = N // 2  # Генерация случайного числа
        n = random.randint(2, m)  # из интервала 2..N/2
        n = 2 * n - 1  # Получение нечетного случайного числа
    return n


def ExtendedEuclid(a, b):
    """Расширенный алгоритм Евклида для нахождения НОД"""
    if not b:
        return a, 1, 0
    d, xx, yy = ExtendedEuclid(b, a % b)
    x = int(yy)
    # согласно лемме о решении линейной комбинации для расширенного алгоритма Евклида:
    y = int(xx - a // b * yy)
    return d, x, y


def GenerateKeyRSA(N):
    """Генерация ключей RSA"""
    p = GeneratePrime(N)   # Генерация простых чисел p и q
    q = GeneratePrime(N)
    while p == q:
        p = GeneratePrime(N)   # Генерация простых чисел p и q
        q = GeneratePrime(N)

    f = (p - 1) * (q - 1)  # Вычисление функции Эйлера
    e = 3  # инициализация e

    t, x, y = ExtendedEuclid(e, f)  # Находим НОД(e,f)
    while t > 1:
        e = e + 2  # генерация e
        t, x, y = ExtendedEuclid(e, f)  # Находим НОД(e,f)

    n = p * q  # Вычисление криптомодуля
    d = x % f  # Вычисление числа d
    return e, d, n


def ModExp(a, b, n):
    """Возведение в степень по модулю"""
    # Получение двоичное записи числа b
    beta = [b % 2]
    b = b // 2
    while b > 0:
        beta.append(b % 2)
        b = b // 2

    d = 1
    for i in range(len(beta) - 1, -1, -1):
        d = (d * d) % n # Получение остатка от деления на n
        # Рекуррентное соотношение
        if beta[i] == 1:
            d = (d * a) % n
    return d


def step1():
    """Генерация ключей"""
    N = 731896679983608908062954695046542151866859438248171349629338126744464505609676195295005917168777707707393114156543347684102186712289705837509128612402093806930245708800868336748316805663985633784235537843102069948768689160359311550728360605672841
    e, d, n = GenerateKeyRSA(N)
    print('Открытый ключ (e, n): ' + str(e) + ', ' + str(n))
    print('Закрытый ключ (d, n): ' + str(d) + ', ' + str(n))


def step2():
    """Шифрование сообщения"""
    message = 0
    e = 0
    n = 0
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
    message = 0
    d = 0
    n = 0
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
        print('Выйти из программы - 0')
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


if __name__ == "__main__":
    start()

