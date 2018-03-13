#!/usr/bin/python3
# encoding utf-8

"""
If you define a class, you call it like a function to create instance.
If you want to customize this step, you can do it by defining a metaclass and
reimplementing its __call__() method in some way
"""
class NoInstances(type):
    def __call__(self, *args, **kwargs):
        raise TypeError("Can't instantiate directly")


# Example
class Spam(metaclass=NoInstances):
    @staticmethod
    def grok(x):
        print('Spam.gork')

# s = Spam()  # Can't instantiate directly


"""
Singleton pattern
"""
class Singleton(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super(Singleton, self).__init__(*args, **kwargs)
        
    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super(Singleton, self).__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


class Spam(metaclass=Singleton):
    def __init__(self):
        print('Creating Spam')

a = Spam()  # Creating Spam
b = Spam()
print(a is b)  # True


