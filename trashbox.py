m = 810


def Eratosphen(n):
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


print(Eratosphen(m))
