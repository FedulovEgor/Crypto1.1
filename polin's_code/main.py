import sys
import time
import random
from random import randint


def mod_exp(a, b, n):
    k = -1
    beta = []

    # Получение двоичное записи числа b
    k = k + 1
    beta.append(b%2)
    b = b // 2
    while b > 0:
        k = k + 1
        beta.append(b%2)
        b = b // 2

    d=1
    for i in range(k,-1,-1):
        d = d*d % n # Получение остатка от деления на n
        # Рекуррентное соотношение
        if beta[i]==1:
            d = d*a % n
    return d


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
    beta.append(b%2)
    b = b // 2
    while b > 0:
        k = k + 1
        beta.append(b%2)
        b = b // 2

    # Повторяем метод Рабина-Миллера r раз
    for j in range(r):
        a = randint(2, n-1) # Получаем случайное основание a
        # Проверяем взаимную простоту a и n
        if euclid(a,n) > 1:
            return False
        # Возведение числа a в степень n-1
        # с помощью метода повторного возведения
        # в квадрат с использованием рекуррентного соотношения
        # и проверки на нетривиальный корень из 1
        d = 1
        for i in range(k,-1,-1):
            x = d
            d = d*d % n # Получение остатка от деления на n
            # Проверка на нетривиальный корень из 1
            if d == 1 and x != 1 and x != n - 1:
                return False
            # Рекуррентное соотношение
            if beta[i]==1:
                d = d*a % n
        # Если НОД(a,n) не равен 1     
        if d != 1:
            return False # n - составное
    return True



def eratosphen(n):
    p = 0
    a = []

    # Получение списка заполненного 1
    for j in range(n+1):
        a.append(1)

    
    j = 2
    # Просматриваем все числа меньше n
    while j*j <= n:
        # Если число не вычеркнуто, то оно - простое
        if a[j] == 1:
            i = j*j
            # Вычеркиваются все числа кратные j
            while i <= n:
                a[i] = 0
                i = i + j
        j = j + 1

    m = 0
    p = []

    # Получаем список простых чисел
    for j in range(2,n+1):
        if a[j] == 1:
            p.append(j)
            
    return p


def is_prime(n):
    p = eratosphen(810) # Получение первых 150 простых чисел
    m = len(p)

    # Сравнение сгенерированного числа n с первыми 150 простыми числами
    for i in range(m):
        # Проверка делится ли число n на одно из первых простых чисел 
        if n % p[i] == 0:
            # Если сгенерированное число n является одним
             # из первых простых чисел,
            if n == p[i]:
                return True # то n - простое
            else:
                return False # иначе n - составное
            
    r = 60 # Количество повторение теста Рабина-Миллера
    return rabin_miller(n, r)


def generate_prime(N):
    m = N // 2 # Генерация случайного числа
    n = randint(2, m) # из интервала 2..N/2
    n = 2 * n - 1 # Получение нечетного случайного числа

    #Пока число не простое, продолжаем генерировать
    while is_prime(n) != True:
        m = N // 2 # Генерация случайного числа
        n = randint(2, m) # из интервала 2..N/2
        n = 2 * n - 1 # Получение нечетного случайного числа
    return n


def extended_euclid(a, b):
    x1 = 0
    x = 1
    y1 = 1
    y = 0

    # Пока делитель не равен 0
    while b > 0:
        q = a // b # находим целую часть от деления a на b

        t = b
        b = a % b # находим остаток от деления a на b
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


def generate_keys_rsa(N):
    t = 0
    x = 0
    f = 0
    
    p = generate_prime(N)  # Генерация простого числа p
    q = generate_prime(N)  # Генерация простого числа q
    f = (p - 1) * (q - 1)  # Вычисление функции Эйлера
    e = 3
    t, x, y = extended_euclid(e, f)  # Находим НОД(e,f)

    # Генерируем простые числа p и q, пока они равны или НОД(e,f) не равен 1
    while p == q or t > 1:
        p = generate_prime(N)  # Генерация простого числа p
        q = generate_prime(N)  # Генерация простого числа q
        f = (p - 1) * (q - 1)  # Вычисление функции Эйлера
        e = e + 2
        t, x, y = extended_euclid(e, f)  # Находим НОД(e,f)
        
    n = p * q #Вычисление криптомодуля 
    d = x % f #Вычисление числа d
    return e, d, n, p, q

def action_0():
    sys.exit(0)

def action_1():
    N = 109417386415705274218097073220403576120037329454492059909138421314763499842889347847179972578912673324976257528997818337970765372440271467435315933543338974563728164539274563715647292635473920374657489365648392736457483
    e_key, d_key, n_key, p, q = generate_keys_rsa(N)
    print('Открытый ключ: ' + str(e_key) + ', ' + str(n_key))
    print('Закрытый ключ: ' + str(d_key) + ', ' + str(n_key))
    print('Простое число p: ' + str(p))
    print('Простое число q: ' + str(q))
    print('')
    start()

        
            

def action_2():
    print('Введите первую часть открытого ключа (e)')
    e_key = input()
    print('Введите вторую часть открытого ключа (n)')
    n_key = input()
    print('Введите сообщение, которое хотите зашифровать')
    message = input()
    if isint(e_key) and isint(n_key) and isint(message):
        start_time=time.perf_counter()
        result = mod_exp(int(message), int(e_key), int(n_key))
        finish_time=time.perf_counter()
        print('Зашифрованное сообщение')
        print(str(result))
        print(f"Время шифрования: {finish_time-start_time:0.15f} секунд")
        print('')
        start()
    else:
        print('Введенные данные некорректны')
        action_2()


def action_3():
    print('Введите первую часть закрытого ключа (d)')
    d_key = input()
    print('Введите вторую часть закрытого ключа (n)')
    n_key = input()
    print('Введите сообщение, которое хотите расшифровать')
    message = input()
    if isint(d_key) and isint(n_key) and isint(message):
        result = 0
        start_time=time.perf_counter()
        result = mod_exp(int(message), int(d_key), int(n_key))
        finish_time=time.perf_counter()
        print('Расшифрованное сообщение')
        print(str(result))
        print(f"Время расшифрования: {finish_time-start_time:0.15f} секунд")
        print('')
        start()
    else:
        print('Введенные данные некорректны')
        action_3()

def start():
    print('МЕНЮ:')
    print('Сгенерировать ключи - 1')
    print('Зашифровать сообщение - 2')
    print('Расшифровать сообщение - 3')
    print('Выход - 0')
    action = input()
    if isint(action):   
        if int(action) == 1:
            action_1()
        elif int(action) == 2:
            action_2()
        elif int(action) == 3:
            action_3()
        elif int(action) == 0:
            action_0()
    else:
        print('Такой команды нет')
        start()

if __name__ == '__main__':
    start()
