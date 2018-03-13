from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice
# Create your views here.

# 定义视图的基本形式, 实际应用中使用 generic view
# def index(request):
#     # 这里可以考虑使用 limit
#     latest_question_list = Question.objects.order_by('-pub_date')[0:5]
#     # template = loader.get_template('polls/index.html')
#     # context = RequestContext(request, {
#     #     'latest_question_list': latest_question_list,
#     # })
#     # return HttpResponse(template.render(context))
#
#     # 快捷方式 render()
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # 对于ListView， 自动生成的context 变量是question_list。
    # 为了覆盖这个行为，我们提供 context_object_name 属性，
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("question {} not found".format(question_id))
#
#     # 便捷方式
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})


class DetailView(generic.DetailView):
    model = Question
    # 默认情况下，通用视图DetailView 使用一个叫做<app name>/<model name>_detail.html的模板
    template_name = 'polls/detail.html'


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = q.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'error_message': "没有选择选项",
            'question': q
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

    # reverse 函数避免了在视图函数中硬编码URL, 这里将返回 'polls/3/results/'
    return HttpResponseRedirect(reverse('polls:results', args=(q.id, )))


