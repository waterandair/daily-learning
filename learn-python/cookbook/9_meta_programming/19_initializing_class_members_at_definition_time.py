#!/usr/bin/python3
# encoding utf-8
import operator
"""
Performing initialization or setup actions at the time of class definition is a classic use of metaclass.
Essentially, a metaclass is triggered at the point of a definition, at which point you can perform additional steps.
"""


class StructTupleMeta(type):
    def __init__(cls, *args,**kwargs):
        super().__init__(*args, **kwargs)
        for n, name in enumerate(cls._fields):
            setattr(cls, name, property(operator.itemgetter(n)))

        
