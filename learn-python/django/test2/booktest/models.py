from django.db import models

class BookInfoManager(models.Manager):
    # 过滤
    def get_queryset(self):
        # return super(BookInfoManager, self).get_queryset().filter(isDelete=False)
        return super(BookInfoManager, self).get_queryset().filter()

    # 创建一个对象
    # 调用:
    # book = BookInfo.books.create_book("倚天屠龙记", datetime.now())
    # book.save()
    def create_book(self, title, pub_date):
        # 调用self.create() 创建
        book = self.create(btitle=title, bpub_date=pub_date, bread=0, bcommet=0, isDelete=False)
        return book

        # book = self.model()
        # book.btitle = title
        # book.bpub_date = pub_date
        # book.bread = 10
        # book.bcomment = 5
        # book.isDelete = False
        # return book

class BookInfo(models.Model):
    btitle = models.CharField(max_length=20, default='')
    bpub_date = models.DateTimeField()
    bread = models.IntegerField(default=0)
    bcommet = models.IntegerField(default=0)
    isDelete = models.BooleanField(default=False)

    books = BookInfoManager()


class HeroInfo(models.Model):
    hname = models.CharField(max_length=20)
    hgender = models.BooleanField(default=True)
    isDelete = models.BooleanField(default=False)
    hcontent = models.TextField(max_length=1000)
    hbook = models.ForeignKey('BookInfo')


class AreaInfo(models.Model):
    """
    自连接
    """
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True)