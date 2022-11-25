from django.shortcuts import render, redirect
import datetime
from .models import Question, OnmkStat
from mo.models import StaffModel


def index(request):
    question_list = Question.objects.order_by('sn')
    context = {'question_list': question_list, 'values': OnmkStat.objects.filter(
        rep_year=datetime.datetime.now().strftime("%Y")
    )}

    if request.user.pk:
        context['staff'] = StaffModel.objects.get(user=request.user)
    return render(request, 'onmkstat/index.html', context)


def new_report(request):
    question_list = Question.objects.order_by('sn')
    context = {'question_list': question_list, 'values': OnmkStat.objects.filter(
        rep_year=datetime.datetime.now().strftime("%Y")
    )}

    if request.user.pk:
        context['staff'] = StaffModel.objects.get(user=request.user)

    # RepFormSet = inlineformset_factory(Rubric, Bb, form=RepForm, extra=1)
    # if request.method == 'POST':
    #     formset = RepFormSet(request.POST, instance=rubric)
    #     if formset.is_valid():
    #         formset.save()
    #     return redirect('onmkstat: index')
    # else:
    #     formset = RepFormSet(instance=rubric)
    return render(request, 'onmkstat/report_form.html', context)
