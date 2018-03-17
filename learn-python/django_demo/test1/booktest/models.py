from django.db import models


class BookInfo(models.Model):
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateTimeField()

    def __str__(self):
        return "%d" % self.pk


class HeroInfo(models.Model):
    hname = models.CharField(max_length=20)
    hgender = models.BooleanField()
    hcontent = models.CharField(max_length=1000)
    hBook = models.ForeignKey('BookInfo')

    def __str__(self):
        return "%d" % self.pk

