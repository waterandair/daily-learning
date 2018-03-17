# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('tagline', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('headline', models.CharField(max_length=255)),
                ('body_text', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('mod_date', models.DateField(auto_now=True)),
                ('n_comments', models.IntegerField(default=0)),
                ('n_pingbacks', models.IntegerField(default=0)),
                ('rating', models.IntegerField(default=0)),
                ('authors', models.ManyToManyField(to='myapp.Author')),
                ('blog', models.ForeignKey(to='myapp.Blog')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30, help_text='姓')),
                ('last_name', models.CharField(max_length=30, help_text='名')),
            ],
        ),
    ]
