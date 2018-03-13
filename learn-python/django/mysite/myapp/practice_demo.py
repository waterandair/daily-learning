from myapp.models import Blog, Entry, Author


# # 创建对象
b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
b.save()  # 没有返回值

# 也可以使用一条语句插入一条数据
b = Blog.objects.create(name="zj2 blog", tagline="zj2 blog tagline")

# 修改
b = Blog.objects.get(pk=1)
b.name = "new name"
b.save()

# 保存ForeignKey和ManyToManyField字段
# 多对一
entry = Entry.objects.get(pk=1)
cheese_blog = Blog.objects.get(name="Cheddar Talk")
entry.blog = cheese_blog
entry.save()
# 多对多
george = Author.objects.create(name="George")
ringo = Author.objects.create(name="Ringo")
entry.authors.add(george, ringo)

# #获取对象
all_entries = Entry.objects.all()
# filter() 满足条件的 支持链式调用
Entry.objects.filter(pub_date__year=2018, mod_date__month=3)
# exclude() 不满足条件的
Entry.objects.exclude(pub_date__year=2018)
# get() 获取单个对象 如果没有获取到对象,会出现一个Entry.DoesNotExist 异常
#                  如果返回多条记录,也会报错,引发 MultipleObjectsReturned


# #限制查询集
# 使用切片语法,等同于 sql中 limit 和 offset 子句, 不支持负索引
Entry.objects.all()[:5]  # (LIMIT 5)
Entry.objects.all()[5:10]  # ( OFFSET 5 LIMIT 5)
# 若要获取一个单一的对象而不是一个列表（例如，SELECT foo FROM bar LIMIT 1）
Entry.objects.order_by('headline')[0]  # 不存在时引发 IndexError
# 等同于
Entry.objects.order_by('headline')[0:1].get()  # 不存在时 引发DoesNotExist


# # 字段查询 (指定WHERE内容)
# SELECT * FROM blog_entry WHERE pub_date <= '2018-01-01';
Entry.objects.filter(pub_date__lte='2018-01-01')
# foreignkey 可以使用字段名加上_id后缀
Entry.objects.filter(blog_id=1)
# 精确匹配
Entry.objects.get(headline="haha")
# 大小写不敏感匹配  (注意get没有值和多个值,都会报错)
Blog.objects.get(name__iexact="zj")
# 大小写敏感的包含关系(sqlite 不敏感)
Blog.objects.get(name__contains="ZJ")


# # 跨关系的查询
# 自动处理join 可以跨越任意深度
Entry.objects.filter(blog__name="zj2 blog")
# 反向,需要使用该模型的小写名称
Blog.objects.filter(entry__headline__contains="entry")
# 跨越多值的关联关系
# 选择所有包含同时满足两个条件的entry的blog，这两个条件是headline 包含 entry 和发表时间是2018 （同一个entry 满足两个条件）
Blog.objects.filter(entry__headline__contains='entry', entry__pub_date__year=2018)
# blog的enrty的headline属性值是“entry”，或者entry的发表时间是2018（两个条件至少满足一个，也可以同时满足):
Blog.objects.filter(entry__headline__contains='entry').filter(entry__pub_date__year=2018)


# Filter 可以引用模型的字段,进行同模型不同字段的比较  F 表达式
# 查找comments 数目多于pingbacks 的Entry
from django.db.models import F
# 支持对F() 对象使用加法、减法、乘法、除法、取模以及幂计算等算术操作
Entry.objects.filter(n_comments__gt=F('n_pingbacks')*2)
# F() 对象中使用双下划线标记来跨越关联关系
Entry.objects.filter(authors__name=F('blog__name'))
from datetime import timedelta
Entry.objects.filter(mod_date__gt=F('pub_date') + timedelta(days=3))


# #查询的快捷方式pk
# 下面三条语句等价
Blog.objects.get(id__exact=1)
Blog.objects.get(id=1)
Blog.objects.get(pk=1)
# 其他
Blog.objects.filter(pk__in=[1, 4, 7])
Blog.objects.filter(pk__gt=1)


# #转义LIKE 语句中的百分号和下划线 django 自动转换百分号和下划线
Entry.objects.filter(headline__contains='%')  # SELECT ... WHERE headline LIKE '%\%%';

# # 缓存和查询集
# 需要多次使用的相同的查询集,尽量复用
# 使用切片或索引来限制查询集将不会填充缓存。
queryset = Entry.objects.all()
print(queryset[5])  # Queries the database
print(queryset[5])  # Queries the database again

queryset = Entry.objects.all()
[entry for entry in queryset]  # Queries the database
print(queryset[5])  # Uses cache
print(queryset[5])  # Uses cache


# # 使用Q 对象进行复杂的查询
# filter() 相当于 “AND” 的。执行更复杂的查询（例如OR 语句），可以使用Q 对象。
from django.db.models import Q
Q(question__startswith='Who') | Q(question__startswith='What')
# 相当于  WHERE question LIKE 'Who%' OR question LIKE 'What%'
# 每个接受关键字参数的查询函数（例如filter()、exclude()、get()）都可以传递一个或多个Q 对象作为位置（不带名的）参数
from polls.models import Question
import datetime
# SELECT * from polls WHERE question LIKE 'Who%' AND (pub_date = '2005-05-02' OR pub_date = '2005-05-06')
Question.objects.get(
    Q(question__startswith='Who'),
    Q(pub_date=datetime(2005, 5, 2)) | Q(pub_date=datetime(2005, 5, 6))
)
# 查询函数可以混合使用Q 对象和关键字参数
# 如果出现Q 对象，它必须位于所有关键字参数的前面
Question.objects.get(
    Q(pub_date=datetime(2005, 5, 2)) | Q(pub_date=datetime(2005, 5, 6)),
    question__startswith='Who')


# # 比较对象



