from booktest import views
from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    path('/', views.index),
    path('^book/([0-9]+)/$', views.detail, name="detail")
]
