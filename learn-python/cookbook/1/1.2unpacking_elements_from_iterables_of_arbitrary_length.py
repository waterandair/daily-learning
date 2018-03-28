#!/usr/bin/python3
# -*- coding utf-8 -*-

# use star expressions
grades = [x for x in range(1, 11)]


def drop_first_last(grades):
    first, *middle, last = grades
    return '%.2f' % (sum(middle)/len(middle))


print(drop_first_last(grades))  # equal like (2 + 3_num_date_time + 4 + 5 + 6 + 7 + 8 + 9) / 8 = 5.50


# another case
record = ('kobe', 'kobe@nba.com', '110', '119')
name, email, *phone_numbers = record
print(name,email,phone_numbers)

# starred variable can also be the first one in the list.
sales_record = [x for x in range(100, 109)]
*trailing_qtrs, current_qtr = sales_record
print(trailing_qtrs,current_qtr)


# It is worth nothing that the star syntax can be especially useful when iterating over a sequence
# of tuples of varying length.
records = [
    ('foo', 1, 2),
    ('bar', 'hello'),
    ('foo', 3, 4),
]


def do_foo(x, y):
    print('foo', x, y)


def do_bar(s):
    print('bar', s)


for tag, *args in records:
    if tag == 'foo':
        do_foo(*args)
    elif tag == 'bar':
        do_bar(*args)

# star unpacking can also be useful when combined with certain kinds of string processing operations
line = 'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false'
uname, *fields, homedir, sh = line.split(':')
print(uname, fields, homedir, sh)  # nobody ['*', '-2', '-2', 'Unprivileged User'] /var/empty /usr/bin/false


# you could use a common throwaway variable name, such as _ or ign(ignored)
record = ('kobe', 50, 123.05, (12, 18, 2012))
name, *_, (*_, year) = record
print(name, year)


# curiosity
items = [1, 10, 7, 4, 5, 9]
def sum(items):
    head, *tail = items

    return head + sum(tail) if tail else head

print(sum(items))




