#!/usr/bin/python3
# -*- coding utf-8 -*-

points = {
    'kobe': 81,
    'wade': 60,
    't-mac': 65,
    'ai': 50,
    'paul': 30
}

# in order to perform useful calculations on the dictionary contents, it is often useful to invert the keys
# and values of the dictionary using zip().
# for example, here is how to find the minimum and maximum point and player's name

min_point = min(zip(points.values(), points.keys()))
print(min_point)  # (30, 'paul')

max_point = max(zip(points.values(), points.keys()))
print(max_point)  # (81, 'kobe')

points_sorted = sorted(zip(points.values(), points.keys()), reverse=True)
print(points_sorted)

# when doing these calculations, be aware that zip() creates an iterator that can only be consumed once
points_and_players = zip(points.values(), points.keys())
print(min(points_and_players))  # (30, 'paul')
# print(max(points_and_players))  # ValueError: max() arg is an empty sequence

# if you try to perform common data reductions on a dictionary,
# you'll find that they only process the key,not the values
print(min(points))  # ai
print(max(points))  # wade

print(min(points.values()))  # 30
print(max(points.values()))  # 81

print(min(points, key=lambda k: points[k]))  # paul
print(max(points, key=lambda k: points[k]))  # kobe

min_value = points[min(points, key=lambda k: points[k])]
print(min_value)  # 30


# in calculations such as min() and max(), the entry with the smallest or largest key will be returned if
# there happen to be duplicate values.
points = {
    'jordan': 100,
    'kobe': 100,
}
print(min(zip(points.values(), points.keys())))  # (100, 'jordan')
print(max(zip(points.values(), points.keys())))  # (100, 'kobe')   'j' is in front of 'k'



