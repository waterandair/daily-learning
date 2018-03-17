from django.shortcuts import render
from django.http import HttpResponse
from booktest.models import BookInfo, AreaInfo
from datetime import date
from django.db.models import F
from datetime import timedelta
from django.db.models import Q
from django.db import connection
# import pdb;  pdb.set_trace() 调试神器


def index(request):
    booklist = BookInfo.books.all()
    return render(request, 'booktest/index.html', {'booklist': booklist})


def detail(request, id):
    book = BookInfo.objects.get(pk=id)
    return render(request, 'booktest/detail.html', {'book': book})

def test(request):
    # 返回结果集
    books = BookInfo.books.all()  # QuerySet
    books = BookInfo.books.filter(btitle='雪山飞狐', bread=58)
    books = BookInfo.books.filter(btitle='雪山飞狐').filter(bread=58)
    books = BookInfo.books.exclude(btitle='射雕英雄传')
    books = BookInfo.books.order_by('bread')  # 正序
    books = BookInfo.books.order_by('-bread')  # 倒序
    books = BookInfo.books.values('btitle')  # 返回字典形式，并且限定返回的字段
    # return HttpResponse([book['btitle'] + ' ' for book in books])
    # return HttpResponse([book.btitle + ' ' + str(book.bread) for book in books])
    # return HttpResponse(books.query)  # 简单查看查询语句

    # 返回单个对象
    book = BookInfo.books.get(pk=2)  # 此君找不到值或找到多个值都会报错，用于unique的字段查询
    # book = BookInfo.books.get(pk=9)  # DoesNotExist
    # book = BookInfo.books.get(isDelete=False)  # MultipleObjectsReturned
    book_total = BookInfo.books.count() # 获取总数
    book = BookInfo.books.first()
    book = BookInfo.books.filter(btitle='雪山飞狐', bread=58).first() # 返回结果集中的第一个对象
    # return HttpResponse(book_total)
    # return HttpResponse(book.btitle)

    # 比较运算符
    # 在前面加个i表示不区分大小写，如iexact、icontains、istarswith、iendswith
    books = BookInfo.books.exclude(btitle__contains='传').exclude(btitle__contains='狐')
    books = BookInfo.books.filter(btitle__endswith='传')
    books = BookInfo.books.filter(btitle__startswith='倚')
    books = BookInfo.books.filter(pk__in=[1, 2, 3])
    books = BookInfo.books.filter(id__gt=3)  # gt, gte, lt, lte : 大于/大于等于/小于/小于等于
    # 对日期类型的属性进行运算
    books = BookInfo.books.filter(bpub_date__year=1980)
    books = BookInfo.books.filter(bpub_date__gt=date(1980, 12, 31))
    books = BookInfo.books.filter(heroinfo__hcontent__contains='八')
    books = BookInfo.books.filter(pk__lt=6)

    # 聚合函数 使用 aggregate()函数返回聚合函数的值
    # 函数：Avg，Count，Max，Min，Sum

    # F 对象 可以使用模型的字段A与字段B进行比较，如果A写在了等号的左边，则B出现在等号的右边，需要通过F对象构造
    books = BookInfo.books.filter(bread__gte=F('bcommet'))
    # 还可以进行运算
    books = BookInfo.books.filter(bread__gte=F('bcommet')*3)
    # 还可以写作“模型名__列名” 进行关联查询
    books = BookInfo.books.filter(isDelete=F('heroinfo__isDelete'))
    # 对于 date/time 字段，可与 timedelta() 进行运算
    books = BookInfo.books.filter(bpub_date__lt=F('bpub_date') + timedelta(days=1))

    # Q 对象 用于封装一组关键字参数，这些关键字参数与“比较与运算符”中的相同
    # Q 对象可以使用&（and）、 |（or）、~(not) 操作符组合起来， 当操作符应用在两个Q对象时，会产生一个新的Q对象
    # 过滤器函数可以传递一个或多个Q对象作为位置参数，如果有多个Q对象，这些参数的逻辑为and
    # 过滤器函数可以混合使用Q对象和关键字参数，所有参数都将and在一起，Q对象必须位于关键字参数的前面
    books = BookInfo.books.filter(Q(pk__lt=3) | Q(bcommet__gt=10))
    books = BookInfo.books.filter(~Q(pk__lt=3))
    return HttpResponse([book.btitle + ' ' for book in books])

def area(request, id):
    area = AreaInfo.objects.get(pk=id)
    parent_area = area.parent
    children_areas = area.areainfo_set.all()
    return HttpResponse([parent_area.name + '->' + area.name + '->' + children_area.name for children_area in children_areas])
