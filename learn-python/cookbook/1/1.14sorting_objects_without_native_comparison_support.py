#!/usr/bin/python
# -*- coding utf-8 -*-
from operator import attrgetter

class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def __str__(self):
        return 'User({})'.format(self.user_id)

    __repr__ = __str__


users = [
    User(5),
    User(2),
    User(11)
]

print(sorted(users, key=lambda u: u.user_id))  # [User(2), User(5), User(11)]


# instead of using lambda, an alternative approach is to use operator.attrgetter()
print(sorted(users, key=attrgetter('user_id')))  # [User(2), User(5), User(11)]


# It is also worth noting that the technique used in this recipe can be applied to
# functions such as min() and max()