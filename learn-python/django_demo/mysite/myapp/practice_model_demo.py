from django_demo.mysite.myapp.models import Blog, Entry, Author


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


# #转义LIKE 语句中的百分号和下划线 django_demo 自动转换百分号和下划线
Entry.objects.filter(headline__contains='%')  # SELECT ... WHERE headline LIKE '%\%%';

# # 缓存和查询集
# 需要多次使用的相同的查询集,尽量复用
# 使用切片或索引来限制查询集将不会填充缓存。
queryset = Entry.objects.all()
print(queryset[5])  # Queries the database
print(queryset[5])  # Queries the database again

queryset = Entry.objects.all()
[entry for entry in queryset]  # Queries the database
print(queryset[5])  # Uses cachep
print(queryset[5])  # Uses cache


# # 使用Q 对象进行复杂的查询
# filter() 相当于 “AND” 的。执行更复杂的查询（例如OR 语句），可以使用Q 对象。
from django.db.models import Q
Q(question__startswith='Who') | Q(question__startswith='What')
# 相当于  WHERE question LIKE 'Who%' OR question LIKE 'What%'
# 每个接受关键字参数的查询函数（例如filter()、exclude()、get()）都可以传递一个或多个Q 对象作为位置（不带名的）参数
from django_demo.mysite.polls.models import Question
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
# 使用标准的Python 比较操作符，即双等于符号：==。在后台，它会比较两个模型主键的值。

# # 删除对象
# 默认会根据 foreignKey 删除关联的记录,可以通过 ForeignKey 的 on_delete 参数自定义
# delete() 是唯一没有在管理器 上暴露出来的查询集方法。这是一个安全机制来防止你意外地请求Entry.objects.delete()，而删除所有 的条目
# e.delete()
Entry.objects.filter(pub_date__year=2005).delete()
b = Blog.objects.get(pk=1)
b.delete()


# # 拷贝模型实例

# # 一次更新多个对象 update
Entry.objects.filter(pub_date__year=2007).update(headline='Everything is the same')
# 若要更新ForeignKey 字段，需设置新的值为你想指向的新的模型实例
b = Blog.objects.get(pk=1)
Entry.objects.all().update(blog=b)
# update() 方法会立即执行并返回查询匹配的行数（如果有些行已经具有新的值，返回的行数可能和被更新的行数不相等）
# 果你想保存查询集中的每个条目并确保每个实例的save() 方法都被调用，你不需要使用任何特殊的函数来处理。只需要迭代它们并调用save()
# 对update 的调用也可以使用F 表达式 来根据模型中的一个字段更新另外一个字段
Entry.objects.all().update(n_pingbacks=F('n_pingbacks') + 1)


# # 关联的对象

# # 一对多关系
# # 前向查询
e = Entry.objects.get(id=2)
e.blog
# 修改关联的对象
b = Blog.objects.create(name='zl', tagline='zl')
e.blog = b
e.save()  # 必须调用save() 才能保存
# 如果 ForeignKey 字段有 null = True 设置,可以分配 None 来删除对应的 关联性
e = Entry.objects.get(id=2)
e.blog = None
e.save()  # "UPDATE blog_entry SET blog_id = NULL ...;"
# 一对多关联关系的前向访问在第一次访问关联的对象时被缓存。以后对同一个对象的外键的访问都使用缓存。
e = Entry.objects.get(id=2)
print(e.blog)  # Hits the database to retrieve the associated Blog.
print(e.blog)  # Doesn't hit the database; uses cached version.
# # 反向查询
# 如果模型I有一个ForeignKey，那么该ForeignKey 所指的模型II实例可以通过一个管理器返回前面有ForeignKey的模型I的所有实例。
# 默认情况下，这个管理器的名字为foo_set，其中foo 是源模型的小写名称。
b = Blog.objects.get(id=1)
b.entry_set.all()  # 返回 Entry 中所有关联到 b 的 记录
# 可以在ForeignKey 定义时设置related_name 参数来覆盖foo_set 的名称
# Entry model 中 blog = ForeignKey(Blog, related_name='entries')
# # 处理关联对象的其它方法
# add(obj1, obj2, ...)  create(**kwargs) remove(obj1, obj2, ...)  clear()

# # 多对多关系
# 多对多关系的两端都会自动获得访问另一端的API
# 属性的名称：定义 ManyToManyField 的模型使用该字段的属性名称，而“反向”模型使用源模型的小写名称加上'_set'
e = Entry.objects.get(id=3)
e.authors.all()  # Returns all Author objects for this Entry.
e.authors.count()
e.authors.filter(name__contains='John')
a = Author.objects.get(id=5)
a.entry_set.all()  # Returns all Entry objects for this Author.

# # 一对一关系
# class EntryDetail(models.Model):
#     entry = models.OneToOneField(Entry)
#     details = models.TextField()
# ed = EntryDetail.objects.get(id=2)
# ed.entry # Returns the related Entry object.
# e = Entry.objects.get(id=2)
# e.entrydetail # returns the related EntryDetail object



