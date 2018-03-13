#!/usr/bin/python
# -*- coding utf-8 -*-


def _odd_iter():
    """所有的奇数"""
    n = 1
    while True:
        n += 2
        yield n


def _not_divisible(n):
    """过滤掉不能除尽的数"""
    return lambda x: x % n > 0


def primes():
    """所有的素数"""
    yield 2
    it = _odd_iter()
    while True:
        n = next(it)
        yield n
        it = filter(_not_divisible(n), it)


def main():
    for i in primes():
        if i < 30:
            print(i)
        else:
            break


if __name__ == '__main__':
    main()


