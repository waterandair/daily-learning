#!/usr/bin/python3
# *-* coding utf-8 *-*
import json
from pprint import pprint
from collections import OrderedDict
"""
The json module provides an easy way to encode and decode data in JSON. The two main functions are
json.dumps() and json.loads(), mirroring the interface used in other serialization libraries,
such as pickle. Here is how you turn a Python data structure into JSON:
"""
data = {
    'name': 'kobe',
    'age': '38',
    'points': 81
}

json_str = json.dumps(data)

print (type(json_str), json_str)  # <class 'str'> '{"age": "38", "points": 81, "name": "kobe"}'

# Here is how you turn a JSON-encoded string back into a Python data structure
data = json.loads(json_str)
print (type(data), data)  # <class 'dict'> {'points': 81, 'name': 'kobe', 'age': '38'}

"""
If you are working with files instead of strings, you can alternatively use 
json.dump() and json.load() to encode and decode JSON data
"""
# Writing JSON data
with open('./test/data.json', 'wt') as f:
    json.dump(data, f)

# Reading data back
with open('./test/data.json', 'rt') as f:
    data = json.load(f)
    print (data)  # {'name': 'kobe', 'age': '38', 'points': 81}


"""
The format of JSON encoding is almost identical to Python syntax except for a few minor changes.For instance,
True is mapped to true, False is mapped to false, and None is mapped to null.
"""
print(json.dumps(False))  # false
data = {
    'a': True,
    'b': False,
    'c': None,
    'd': 'Hello'
}
print(json.dumps(data)) # {"d": "Hello", "b": false, "c": null, "a": true}


"""
consider using the pprint() function in the pprint() function in the pprint module.
This will alphabetize the keys and output a dictionary in a more sane way.
"""


"""
Normally , JSON decoding will create dicts or lists from the supplied data. If you want to create different kinds of 
objects, supply the object_pairs_hook or object_hook to json.loads()
For example, here is how you would decode JSON data, preserving its order in an OrderedDict
"""
s = '{"name": "ACME", "shares": 50, "price": 490.1}'
data = json.loads(s, object_pairs_hook=OrderedDict)
print (data)  # OrderedDict([('name', 'ACME'), ('shares', 50), ('price', 490.1)])

# Here is how you could turn a JSON dictionary into a python object
class JSONObject:
    def __init__(self, d):
        self.__dict__ = d

temp = JSONObject(data)
print (temp.name)  # ACME
data = json.loads(s, object_hook=JSONObject)
print (data.name)  # ACME

"""
There are a few options that can be useful for encoding JSON. If you would like the output to be nicely formatted, you 
can use the indent argument to json.dumps(). This cause the output to be pretty printed in a format similar to that with 
the pprint() function.
"""
data = {
    'name': 'kobe',
    'age': '38',
    'points': 81,
    'friends': [
        {'name': 'wade', 'age': 35},
        {'name': 'ai', 'age': 40}
    ]
}
print (json.dumps(data, indent=4))
"""
{
    "age": "38",
    "name": "kobe",
    "friends": [
        {
            "age": 35,
            "name": "wade"
        },
        {
            "age": 40,
            "name": "ai"
        }
    ],
    "points": 81
}
"""

"""
If you want the keys to be sorted on output, used the sort_keys argument
"""
print(json.dumps(data, sort_keys=True, indent=4))
"""
{
    "age": "38",
    "friends": [
        {
            "age": 35,
            "name": "wade"
        },
        {
            "age": 40,
            "name": "ai"
        }
    ],
    "name": "kobe",
    "points": 81
}

"""


"""
If you want to serialize instances, you can supply a function that takes an instance as input and returns a dictionary 
that can be serialized
"""


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def serialize_instance(obj):
    d = { '__classname__': type(obj).__name__ }
    d.update(vars(obj))
    return d


# If you want to get an instance back, you could write code like this:
# Dictionary mapping names to known classes
classes = {
    'Point': Point
}

def unserialize_object(d):
    clsname = d.pop('__classname__', None)
    if clsname:
        cls = classes[clsname]
        obj = cls.__new__(cls)
        for key, value in d.items():
            setattr(obj, key, value)
        return obj
    else:
        return d

p = Point(2, 3)
s = json.dumps(p, default=serialize_instance)
print (s)  # {"__classname__": "Point", "y": 3_num_date_time, "x": 2}
s = json.loads(s, object_hook=unserialize_object)
print (s)  # <__main__.Point object at 0x7f780a4cf6d8>
print (s.x, s.y)  # 2 3_num_date_time