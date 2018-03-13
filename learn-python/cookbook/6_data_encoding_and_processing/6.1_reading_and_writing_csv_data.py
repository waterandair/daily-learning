#!/usr/bin/python3
# *-* coding utf-8 *-*
import csv
from collections import namedtuple
import re
# ***************** Read *****************
"""
Here's how you would read the data as a sequence of tuples
"""
with open('./test/stock.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        pass
"""
Since such indexing can often be confusing, this is one place where you might want to consider the use of named tuples
This would allow you to use the column headers such as row.Symbol, row.Price instead of indices.
It should be noted that this only works if the column headers are valid Python identifiers.
"""
with open('./test/stock.csv') as f:
    f_csv = csv.reader(f)
    headings = next(f_csv)
    Row = namedtuple('Row', headings)
    for r in f_csv:
        row = Row(*r)
        print (row.Symbol, row.Price)


"""
Another alternative is to read the data as a sequence of dictionary instead.
"""
with open('./test/stock.csv') as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
        print (row)
        # {'Symbol': 'AA', 'Change': '-0.18', 'Time': '9:36am', 'Date': '6/11/2007', 'Price': '39.48', 'Volume': '181800'}
        print (row['Symbol'], row['Price'])
        # AA 39.48


# ***************** Write *****************
""" 
To write CSV data, you also use the CSV module but create a write object
"""
headers = ['Symbol','Price','Date','Time','Change','Volume']
rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
        ('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
        ('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000),
       ]
with open('./test/stock2.csv', 'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)

"""
If you have the data as a sequence of dictionaries, do this
"""
headers = ['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
rows = [{'Symbol':'AA', 'Price':39.48, 'Date':'6/11/2007',
          'Time':'9:36am', 'Change':-0.18, 'Volume':181800},
        {'Symbol':'AIG', 'Price': 71.38, 'Date':'6/11/2007',
          'Time':'9:36am', 'Change':-0.15, 'Volume': 195500},
        {'Symbol':'AXP', 'Price': 62.58, 'Date':'6/11/2007',
          'Time':'9:36am', 'Change':-0.46, 'Volume': 935000},
        ]

with open('./test/stock3.csv', 'w') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    f_csv.writerows(rows)


"""
By default, the csv library is programmed to understand CSV encoding rules used by Microsoft Excel.This is probably the
most common variant, and will likely give you the best compatibility.
However, if you consult the documentation for csv, you'll see a few ways to tweak the encoding to different format
For example, if you want to read tab-delimited data instead:
"""
# Example of reading tab-separated values
# with open('./test2/stock.tsv') as f:
#     f_tsv = csv.reader(f, delimiter='\t')
#     for row in f_tsv:
#         pass


"""
To avoid namedtuple fail with a ValueError exception, you might have to scrub the headers firs.
For instance , carrying a regex substitution on nonvalid identify characters like this:
"""
with open('./test/stock4.csv') as f:
    f_csv = csv.reader(f)
    headers = [re.sub('[^a-zA-Z_]', '_', h) for h in next(f_csv)]
    Row = namedtuple('Row', headers)
    for r in f_csv:
        row = Row(*r)
        print (row)
        # Row(S_y_m_b_o_l='AA', Price='39.48', Date='6/11/2007', Time='9:36am', Change='-0.18', Volume='181800')


"""
It's also important to emphasize that csv does not try to interpreter the data or convert it to a type
other than a string. If such conversions are important, that is something you'll need to do yourself.
Here is one example of performing extra type conversions on CSV data:
"""
col_types = [str, float, str, str, float, int]
with open('./test/stock.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        row = tuple(convert(value) for convert, value in zip(col_types, row))
        print (row)


"""
Alternatively, here is an example of converting selected fields of dictionaries
"""
field_types = [
    ('Price', float),
    ('Change', float),
    ('Volume', int)
]
with open('./test/stock.csv') as f:
    for row in csv.DictReader(f):
        row.update((key, conversion(row[key])) for key, conversion in field_types)
        print (row)