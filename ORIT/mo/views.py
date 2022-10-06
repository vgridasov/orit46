import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from .models import BedSpaceNumberModel, StaffModel, MOUnitModel
from arolog.models import AROLogModel


@method_decorator(login_required, name='dispatch')
class BedSpaceNumberListView(generic.ListView):
    paginate_by = 10

    def get_queryset(self):
        return BedSpaceNumberModel.objects.order_by('-edit_date')


class BedSpaceCreateView(LoginRequiredMixin, generic.CreateView):
    model = BedSpaceNumberModel
    template_name = 'arolog/new_rec.html'
    fields = ["num", "note"]
    success_url = '/my/'

    def form_valid(self, form):
        form.instance.mo = StaffModel.objects.get(user=self.request.user).mo
        form.instance.mo_unit = StaffModel.objects.get(user=self.request.user).mo_unit

        return super().form_valid(form)


class MOUnitModelListView(LoginRequiredMixin, generic.ListView):
    model = MOUnitModel
    template_name = 'mo/mou_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['aro_log'] = AROLogModel.objects.filter(
            reg_datetime__date=datetime.datetime.today().date(),
        ).order_by('mo_unit', '-reg_datetime')

        return context


class MOUitDetailView(LoginRequiredMixin, generic.DetailView):
    model = MOUnitModel
    template_name = 'mo/mou_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['aro_logs'] = AROLogModel.objects.filter(
            mo_unit__pk=self.object.pk
        ).order_by('-reg_datetime')

        context['aro_logs_today'] = AROLogModel.objects.filter(
            reg_datetime__date=datetime.datetime.today().date(),
            mo_unit__pk=self.object.pk
        ).order_by('-reg_datetime')

        context['aro_logs_num'] = context['aro_logs'].count()
        context['aro_logs_today_num'] = context['aro_logs_today'].count()

        return context
