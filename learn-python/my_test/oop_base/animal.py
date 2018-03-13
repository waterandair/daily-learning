#!/usr/bin/python
# -*- coding utf-8 -*-


class Animal(object):
    def run(self):
        print('Animal is running……')


class Dog(Animal):
    def run(self):
        print('Dog is running……')


class Cat(Animal):
    def run(self):
        print('Cat is running……')


def run_twice(animal):
    animal.run()
    animal.run()


a = Animal()
d = Dog()
c = Cat()

print('a is Animal?', isinstance(a, Animal))  # True
print('a is Dog?', isinstance(a, Dog))  # False

print('d is Animal?', isinstance(d, Animal))  # True
print('d is Dog?', isinstance(d, Animal))  # True
print('d is Cat?', isinstance(d, Cat))  # false

run_twice(c)


