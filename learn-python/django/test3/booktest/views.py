from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from booktest.models import BookInfo

def index(request):
    booklist = BookInfo.objects.all()
    template = loader.get_template('booktest/index.html')
    context = {'booklist': booklist}
    return HttpResponse(template.render(context))

def detail(request, id):
    book = BookInfo.objects.get(pk=id)
    template = loader.get_template('booktest/detail.html')
    context = {'book': book}
    return HttpResponse(template.render(context))


# Create your views here.
