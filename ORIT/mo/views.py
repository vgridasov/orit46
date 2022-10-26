from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.decorators import method_decorator
from django.views import generic
from .models import BedSpaceNumberModel, StaffModel, MOUnitModel
from arolog.models import AROLogModel


# Timedelta value
DELTA = -16
dt = datetime.combine(timezone.now().date(), datetime.min.time()) + timedelta(hours=DELTA)


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
            reg_datetime__gte=dt,
        ).order_by('mo_unit', '-reg_datetime')

        return context


class MOUitDetailView(LoginRequiredMixin, generic.DetailView):
    model = MOUnitModel
    template_name = 'mo/mou_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['object_list'] = AROLogModel.objects.filter(
            reg_datetime__gte=dt,
            mo_unit__pk=self.object.pk
        ).order_by('s_dyn', '-reg_datetime')

        # Количество занятых коек
        occ_bed_num = AROLogModel.objects.exclude(
            s_dyn='5'  # Исключаем пациентов с летальным исходом
        ).filter(
            mo_unit__pk=self.object.pk,
            reg_datetime__gte=dt
        ).count()

        # Количество свободных коек
        if self.object.get_bed_num():
            context['free_bed_num'] = self.object.get_bed_num() - occ_bed_num
            context['free_bed_percent'] = round(context['free_bed_num'] / self.object.get_bed_num() * 100, 1)
        else:
            context['free_bed_num'] = '-'
            context['free_bed_percent'] = '-'

        # количество поступлений на сегодня
        context['curr_new_num'] = AROLogModel.objects.filter(
            mo_unit__pk=self.object.pk,
            reg_datetime__gte=dt,
            s_dyn='1'
        ).count()

        # Количество ухудшений состояний на сегодня
        context['curr_decline_num'] = AROLogModel.objects.filter(
            mo_unit__pk=self.object.pk,
            reg_datetime__gte=dt,
            s_dyn='4'
        ).count()

        # количество летальных на сегодня
        context['curr_lethal_num'] = AROLogModel.objects.filter(
            mo_unit__pk=self.object.pk,
            reg_datetime__gte=dt,
            s_dyn='5'
        ).count()

        return context
