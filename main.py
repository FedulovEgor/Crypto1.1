import random
import math

e, d, n = 0, 0, 0


def Eratosphen(n):
    """Генерирует решето Эратосфена"""
    # список заполняется значениями от 0 до n
    a = []
    for i in range(n + 1):
        a.append(i)

    # Вторым элементом является единица,
    # которую не считают простым числом
    # забиваем ее нулем.
    a[1] = 0

    # начинаем с 3-го элемента
    i = 2
    while i <= n:
        # Если значение ячейки до этого
        # не было обнулено,
        # в этой ячейке содержится
        # простое число.
        if a[i] != 0:
            # первое кратное ему
            # будет в два раза больше
            j = i + i
            while j <= n:
                # это число составное,
                # поэтому заменяем его нулем
                a[j] = 0
                # переходим к следующему числу,
                # которое кратно i
                # (оно на i больше)
                j = j + i
        i += 1

    # Превращая список во множество,
    # избавляемся от всех нулей кроме одного.
    a = set(a)
    # удаляем ноль
    a.remove(0)
    return a


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
    P = Eratosphen(810)

    for el in P:
        if (n % el) == 0:
            if n == el:
                return True
            else:
                return False
    r = 50  # Количество повторений теста Рабина-Миллера
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
    return e, d, n


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


def step1():
    global e, d, n
    N = 10 ** 20
    e, d, n = GenerateKeyRSA(N)
    print('Открытый ключ (e, n): ' + str(e) + ', ' + str(n))
    print('Закрытый ключ (d, n): ' + str(d) + ', ' + str(n))


def step2():
    global e, n
    try:
        # print('Введите первую часть открытого ключа (e)')
        # e = int(input())
        # print('Введите вторую часть открытого ключа (n)')
        # n = int(input())
        print('Введите сообщение, которое хотите зашифровать')
        message = int(input())
    except ValueError:
        print('Введенные данные некорректны')
        step2()

    result = ModExp(message, e, n)
    print('Зашифрованное сообщение')
    print(str(result))


def step3():
    global d, n
    try:
        # print('Введите первую часть закрытого ключа (d)')
        # d = int(input())
        # print('Введите вторую часть закрытого ключа (n)')
        # n = int(input())
        print('Введите сообщение, которое хотите расшифровать')
        message = int(input())
    except ValueError:
        print('Введенные данные некорректны')
        step3()

    result = ModExp(message, d, n)
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
