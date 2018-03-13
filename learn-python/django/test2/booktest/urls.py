# -*- coding utf-8 -*-
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^book/([0-9]+)$', views.detail, name='detail'),
    url(r'^test$', views.test, name='test'),
    url(r'^area/([0-9]+)$', views.area, name='area')
]
