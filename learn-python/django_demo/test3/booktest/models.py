from django.db import models

# Create your models here.

class BookInfo(models.Model):
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateField()

    def __str__(self):
        return "%d" % self.pk


class HeroInfo(models.Model):
    hname = models.CharField(max_length=20)
    hgender = models.BooleanField()
    hcontent = models.CharField(max_length=100)
    hBook = models.ForeignKey('BookInfo', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "%d" % self.pk



