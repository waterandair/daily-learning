#!/usr/bin/python
# -*- coding utf-8 -*-


# 关键词参数
def print_score(**kw):
    print("      Name    Score")
    print("-------------------")
    for name, score in kw.items():
        print("%10s    %d" % (name, score))


print_score(kobe=100, wade=90, tmac=85)

data = {
    'KOBE': 100,
    'WADE': 99,
    'T-MAC': 98
}
print_score(**data)


# 命名关键词参数 可以用 if ‘gender’ in kw 判断是否传入了该参数
def print_info(name, *, gender, city="BeiJing", age):
    print('''
    
    Personal Info
    -------------
    name:    %s
    gender:  %s
    city:    %s
    age:     %s
    
    ''' % (name, gender, city, age))


print_info('kobe', gender='male', age=20)
print_info('wade', gender='male', age=18, city='shanghai')
