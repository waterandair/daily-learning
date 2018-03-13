#!/usr/bin/python3
# -*- coding utf-8 -*-

class Person:
    def __init__(self, name):
        self.name = name

    # Getter function
    @property
    def name(self):
        return self._name

    # Setter function
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._name = value

    # Delecter function
    @name.deleter
    def name(self):
        raise AttributeError("can't delete attribute")


class SubPerson(Person):
    @property
    def name(self):
        print('Getting name')
        return super(SubPerson, self).name

    @name.setter
    def name(self, value):
        print('setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)

    @name.deleter
    def name(self):
        print('deleting name')
        super(SubPerson, SubPerson).name.__delete__(self)


s = SubPerson('Kobe')  # setting name to Kobe
print(s.name)  # Getting name \n Kobe
s.name = 'Wade'  # setting name to Wade

"""
If you only want to extend one of the methods of a property, use code such as the following:
"""
class SubPerson(Person):
    @Person.name.getter
    def name(self):
        print('Getting name')
        return super(SubPerson, self).name
# Or, alternatively, for just the setter, use this code:

class SubPerson(Person):
    @Person.name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)