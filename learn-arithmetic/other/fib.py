def fib1(n):
    i, a, b = 0, 0, 1

    while i < n:
        a, b = b, a+b
        i += 1

    return a


def fib2(n):
    if n <= 2:
        if n <= 0:
            return
        else:
            return 1
    res = fib2(n-1) + fib2(n-2)
    return res


def fib3(a, b, n):
    if n <= 2:
        if n <= 0:
            return
        else:
            return b
    return fib3(b, a + b, n - 1)


if __name__ == '__main__':
    # 0 1 1 2 3
    print(fib1(6))
    print(fib2(6))
    print(fib3(1, 1, 6))
