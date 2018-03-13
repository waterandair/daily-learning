#!/usr/bin/python
# -*- coding utf-8 -*-
from operator import itemgetter
from itertools import groupby
from collections import defaultdict

# the itertools.groupby() function is particularly useful for grouping data together like this.
rows = [
    {'address': '5412 N CLARK', 'date': '07/01/2012'},
    {'address': '5148 N CLARK', 'date': '07/04/2012'},
    {'address': '5800 E 58TH', 'date': '07/02/2012'},
    {'address': '2122 N CLARK', 'date': '07/03/2012'},
    {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
    {'address': '1060 W ADDISON', 'date': '07/02/2012'},
    {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
    {'address': '1039 W GRANVILLE', 'date': '07/04/2012'},
]

# sort by the desired filed first
# an important preliminary step is sorting the data according to the field of interest
rows.sort(key=itemgetter('date'))

# Iterate in groups
for date, items in groupby(rows, key=itemgetter('date')):
    print(date)
    for i in items:
        print('     %s' % i)

# 07/01/2012
#      {'date': '07/01/2012', 'address': '5412 N CLARK'}
#      {'date': '07/01/2012', 'address': '4801 N BROADWAY'}
# 07/02/2012
#      {'date': '07/02/2012', 'address': '5800 E 58TH'}
#      {'date': '07/02/2012', 'address': '5645 N RAVENSWOOD'}
#      {'date': '07/02/2012', 'address': '1060 W ADDISON'}
# 07/03/2012
#      {'date': '07/03/2012', 'address': '2122 N CLARK'}
# 07/04/2012
#      {'date': '07/04/2012', 'address': '5148 N CLARK'}
#      {'date': '07/04/2012', 'address': '1039 W GRANVILLE'}


# if memory is no concern, it may be faster to do this than to first sort the records and iterate using groupby()
rows_by_date = defaultdict(list)
for row in rows:
    rows_by_date[row['date']].append(row)
print(rows_by_date.items())
