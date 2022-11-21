from django.shortcuts import render
from .models import Question, OnmkStat


def index(request):
    question_list = Question.objects.order_by('sn')
    context = {'question_list': question_list}
    return render(request, 'onmkstat/index.html', context)
