import django.utils.timezone as timezone

from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=30, null=False, blank=False, help_text="姓")
    last_name = models.CharField(max_length=30, help_text="名")


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Entry(models.Model):

    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    mod_date = models.DateTimeField(default=timezone.now)
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField(default=0)
    n_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.headline