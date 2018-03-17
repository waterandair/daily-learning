# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('btitle', models.CharField(max_length=20, default='')),
                ('bpub_date', models.DateTimeField()),
                ('bread', models.IntegerField(default=0)),
                ('bcommet', models.IntegerField(default=0)),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='HeroInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('hname', models.CharField(max_length=20)),
                ('hgender', models.BooleanField(default=True)),
                ('isDelete', models.BooleanField(default=False)),
                ('hcontent', models.TextField(max_length=1000)),
                ('hbook', models.ForeignKey(to='booktest.BookInfo')),
            ],
        ),
    ]
