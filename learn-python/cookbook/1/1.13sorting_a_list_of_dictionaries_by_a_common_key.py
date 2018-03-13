#!/usr/bin/python
# -*- coding utf-8 -*-
from operator import itemgetter
rows = [
    {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
    {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
    {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
    {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
]

rows_by_fname = sorted(rows, key=itemgetter('fname'))
rows_by_uid = sorted(rows, key=itemgetter('uid'))

print(rows_by_fname)
# [
#     {'lname': 'Jones', 'uid': 1004, 'fname': 'Big'},
#     {'lname': 'Jones', 'uid': 1003, 'fname': 'Brian'},
#     {'lname': 'Beazley', 'uid': 1002, 'fname': 'David'},
#     {'lname': 'Cleese', 'uid': 1001, 'fname': 'John'}
# ]

print(rows_by_uid)
# [
#     {'lname': 'Cleese', 'uid': 1001, 'fname': 'John'},
#     {'lname': 'Beazley', 'uid': 1002, 'fname': 'David'},
#     {'lname': 'Jones', 'uid': 1003, 'fname': 'Brian'},
#     {'lname': 'Jones', 'uid': 1004, 'fname': 'Big'}
# ]

# the itemgetter() function can also accept multiple keys
rows_by_lfname = sorted(rows, key=itemgetter('lname', 'fname'))
print(rows_by_lfname)
# [
#     {'lname': 'Beazley', 'uid': 1002, 'fname': 'David'},
#     {'lname': 'Cleese', 'uid': 1001, 'fname': 'John'},
#     {'lname': 'Jones', 'uid': 1004, 'fname': 'Big'},
#     {'lname': 'Jones', 'uid': 1003, 'fname': 'Brian'}
# ]

# the functionality of itemgetter() is sometimes replaced by lambda expressions
# this solution often works just fine.However, the solution involving itemgetter() typically runs a bit faster
rows_by_fname = sorted(rows, key=lambda r: r['fname'])
rows_by_lfname = sorted(rows, key=lambda r: (r['lname'], r['fname']))

# last but not least, don't forget that the technique shown in this recipe can be applied to functions
# such as min() and max()
print(max(rows, key=itemgetter('uid')))
print(min(rows, key=itemgetter('uid')))
