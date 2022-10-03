import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from .models import AROLogModel
from mo.models import StaffModel, BedSpaceNumberModel, MOUnitModel


def index(request):
    context = {'title': 'Добро пожаловать!'}
    if request.user.pk:
        context['staff'] = StaffModel.objects.get(user=request.user)
    return render(request, 'arolog/welcome.html', context)


@method_decorator(login_required, name='dispatch')
class Home(generic.ListView):
    template_name = 'arolog/home.html'

    def get_queryset(self):
        # возврат записей в зависимости от роли пользователя (все или только свои)
        #
        if StaffModel.objects.get(user=self.request.user).is_unit_only:
            return AROLogModel.objects.filter(
                registrator__user=self.request.user,
                reg_datetime__date=datetime.datetime.today().date()
            ).order_by('s_dyn', '-reg_datetime')
        else:
            return AROLogModel.objects.filter(
                reg_datetime__date=datetime.datetime.today().date()
            ).order_by('mo_unit', 's_dyn', '-reg_datetime')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['staff'] = StaffModel.objects.get(user=self.request.user)  # contains title, fio, mo & mo_unit fields

        if StaffModel.objects.get(user=self.request.user).is_unit_only:
            # Коечный фонд своего отделения:
            # кол-во занятых коек отделения текущего пользователя равно
            # кол-ву сегодняшних записей для отделения текущего пользователя, за исключением летальных
            mou = context['staff'].mo_unit
            if mou:
                occ_bed_num = AROLogModel.objects.exclude(
                    s_dyn='5'  # Исключаем пациентов с летальным исходом
                ).filter(
                    mo_unit=mou,
                    reg_datetime__date=datetime.datetime.now().date()
                ).count()
                context['occ_bed_num'] = occ_bed_num
                if BedSpaceNumberModel.objects.filter(mo_unit=mou):
                    context['bed_num'] = BedSpaceNumberModel.objects.filter(mo_unit=mou).latest().num
                    if context['bed_num'] > 0:
                        context['free_bed_num'] = context['bed_num'] - occ_bed_num
                        context['free_bed_percent'] = round(context['free_bed_num'] / context['bed_num'] * 100, 1)
                    else:
                        context['bed_num'] = 'нет данных'
                        context['free_bed_num'] = 'нет данных'
                        context['free_bed_percent'] = '-'
        else:
            context['curr_new_num'] = AROLogModel.objects.filter(
                reg_datetime__date=datetime.datetime.today().date(),
                s_dyn='1'
            ).count()
            context['curr_decline_num'] = AROLogModel.objects.filter(
                reg_datetime__date=datetime.datetime.today().date(),
                s_dyn='4'
            ).count()
            context['curr_lethal_num'] = AROLogModel.objects.filter(
                reg_datetime__date=datetime.datetime.today().date(),
                s_dyn='5'
            ).count()

            tml = AROLogModel.objects.filter(
                            reg_datetime__gte=datetime.datetime.today().date()
                            ).values_list('mo_unit', flat=True).order_by('mo_unit').distinct()
            context['today_mou_list'] = tml

        return context


@method_decorator(login_required, name='dispatch')
class AListView(generic.ListView):
    paginate_by = 10

    def get_queryset(self):
        return AROLogModel.objects.all().order_by('-edit_datetime')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['staff'] = StaffModel.objects.get(user=self.request.user)  # contains title, fio, mo & mo_unit fields

        return context


@method_decorator(login_required, name='dispatch')
class ATodayListView(generic.ListView):
    paginate_by = 10

    def get_queryset(self):
        return AROLogModel.objects.filter(
            reg_datetime__date=datetime.datetime.today().date()
        ).order_by('mo_unit', 's_dyn', '-edit_datetime')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['staff'] = StaffModel.objects.get(user=self.request.user)  # contains title, fio, mo & mo_unit fields

        return context


@method_decorator(login_required, name='dispatch')
class AMyListView(generic.ListView):
    template_name = 'arolog/home.html'
    paginate_by = 10

    def get_queryset(self):
        return AROLogModel.objects.filter(
            registrator__user=self.request.user
        ).order_by('s_dyn', '-reg_datetime')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['staff'] = StaffModel.objects.get(user=self.request.user)  # contains title, fio, mo & mo_unit fields
        mou = context['staff'].mo_unit

        # Коечный фонд своего отделения
        if mou:
            occ_bed_num = AROLogModel.objects.exclude(
                s_dyn='5'  # Исключаем пациентов с летальным исходом
            ).filter(
                mo_unit=mou,
                reg_datetime__date=datetime.datetime.now().date()
            ).count()
            context['occ_bed_num'] = occ_bed_num
            if BedSpaceNumberModel.objects.filter(mo_unit=mou):
                context['bed_num'] = BedSpaceNumberModel.objects.filter(mo_unit=mou).latest().num
                if context['bed_num'] > 0:
                    context['free_bed_num'] = context['bed_num'] - occ_bed_num
                    context['free_bed_percent'] = round(context['free_bed_num'] / context['bed_num'] * 100, 1)
                else:
                    context['bed_num'] = 'нет данных'
                    context['free_bed_num'] = 'нет данных'
                    context['free_bed_percent'] = '-'
        return context


@method_decorator(login_required, name='dispatch')
class ADetailView(generic.DetailView):
    model = AROLogModel
    template_name = 'arolog/arolog_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['staff'] = StaffModel.objects.get(user=self.request.user)  # contains title, fio, mo & mo_unit fields

        return context


@method_decorator(login_required, name='dispatch')
class SearchResultsView(generic.ListView):
    model = AROLogModel
    paginate_by = 25
    template_name = 'arolog/search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if StaffModel.objects.get(user=self.request.user).is_unit_only:
            object_list = AROLogModel.objects.filter(
                registrator__user=self.request.user,
                mh_num__icontains=query  # поиск по номеру истории болезни
            ).distinct().order_by('-edit_datetime')
        else:
            object_list = AROLogModel.objects.filter(
                mh_num__icontains=query
            ).distinct().order_by('mo_unit', '-edit_datetime')

        return object_list

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['staff'] = StaffModel.objects.get(user=self.request.user)  # contains title, fio, mo & mo_unit fields

        return context


class ACreateView(LoginRequiredMixin, generic.CreateView):
    model = AROLogModel
    template_name = 'arolog/new_rec.html'
    fields = [
        "mh_num",  # 'Номер истории болезни')
        "age",  # 'Возраст')
        "to_hosp_date",  # 'Дата поступления в МО')
        "to_unit_date",  # 'Дата поступления в отделение')
        "diagnosis",  # 'Основной диагноз (MKБ-10)')
        "oper_date",  # 'Операция (дата-время завершения)')
        "oper_name",  # 'Операция (наименование)')
        "mind",  # 'Степень угнетения сознания (по Коновалову)'
        "vent",  # Статус ИВЛ
        "s_dyn",  # 'Динамика состояния'
        "note"  # 'Примечания')
    ]

    def form_valid(self, form):
        form.instance.mo = StaffModel.objects.get(user=self.request.user).mo
        form.instance.mo_unit = StaffModel.objects.get(user=self.request.user).mo_unit
        form.instance.registrator = StaffModel.objects.get(user=self.request.user)

        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['staff'] = StaffModel.objects.get(user=self.request.user)  # contains title, fio, mo & mo_unit fields

        return context


class AUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = AROLogModel
    template_name = 'arolog/new_rec.html'
    fields = [
        "mh_num",  # 'Номер истории болезни')
        "age",  # 'Возраст')
        "to_hosp_date",  # 'Дата поступления в МО')
        "to_unit_date",  # 'Дата поступления в отделение')
        "diagnosis",  # 'Основной диагноз (MKБ-10)')
        "oper_date",  # 'Операция (дата-время завершения)')
        "oper_name",  # 'Операция (наименование)')
        "mind",  # 'Степень угнетения сознания (по Коновалову)'
        "vent",  # Статус ИВЛ
        "s_dyn",  # 'Динамика состояния'
        "note"  # 'Примечания')
    ]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['staff'] = StaffModel.objects.get(user=self.request.user)  # contains title, fio, mo & mo_unit fields

        return context
