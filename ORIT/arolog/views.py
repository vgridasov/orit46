from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.utils.decorators import method_decorator
from django.views import generic
from .models import AROLogModel
from mo.models import StaffModel, BedSpaceNumberModel, MOUnitModel


# Timedelta value
DELTA = -8


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
                reg_datetime__gte=timezone.now().date() + timedelta(hours=DELTA)
            ).order_by('s_dyn', '-reg_datetime')
        else:
            return AROLogModel.objects.filter(
                reg_datetime__gte=timezone.now().date() + timedelta(hours=DELTA)
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
                    reg_datetime__gte=timezone.now().date() + timedelta(hours=DELTA)
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
            # Информация по всем отделениям на сегодня
            #
            # общее количество записей на сегодня
            context['curr_log_num'] = AROLogModel.objects.filter(
                reg_datetime__gte=timezone.now().date() + timedelta(hours=DELTA)
            ).count()

            # количество поступлений на сегодня
            context['curr_new_num'] = AROLogModel.objects.filter(
                reg_datetime__gte=timezone.now().date() + timedelta(hours=DELTA),
                s_dyn='1'
            ).count()

            # Количество ухудшений состояний на сегодня
            context['curr_decline_num'] = AROLogModel.objects.filter(
                reg_datetime__gte=timezone.now().date() + timedelta(hours=DELTA),
                s_dyn='4'
            ).count()

            # количество летальных на сегодня
            context['curr_lethal_num'] = AROLogModel.objects.filter(
                reg_datetime__gte=timezone.now().date() + timedelta(hours=DELTA),
                s_dyn='5'
            ).count()

            # Коечный фонд
            """ 
            тут учитываются только подразделения, которые вносили записи сегодня!
            есть потенциальная ошибка - если в МО ненулевой коечный фонд, но при этом сегодня не было внесено 
            ни одной записи (например, все койки отделения свободны), 
            то коечный фонд этого отделения не будет учтен в общей сумме!
            подумать, как это исправить!
            """

            total_bed_num = 0
            total_free_bed_num = 0

            # получение списка подразделений с записями на сегодня
            tml = AROLogModel.objects.filter(
                reg_datetime__gte=timezone.now().date() + timedelta(hours=DELTA)
            ).values_list('mo_unit', flat=True).order_by('mo_unit').distinct()
            mou_list = []
            for m in tml:
                total_bed_num = total_bed_num + BedSpaceNumberModel.objects.filter(mo_unit=m).latest().num
                total_free_bed_num = total_free_bed_num + (
                        BedSpaceNumberModel.objects.filter(mo_unit=m).latest().num -
                        AROLogModel.objects.filter(
                            reg_datetime__gte=timezone.now().date() + timedelta(hours=DELTA),
                            mo_unit=m
                        ).count() +
                        AROLogModel.objects.filter(
                            reg_datetime__gte=timezone.now().date() + timedelta(hours=DELTA),
                            s_dyn='5',  # летальные
                            mo_unit=m
                        ).count()
                )

                mou = {
                    'obj': MOUnitModel.objects.get(pk=m),  # подразделение
                    'bed_num': MOUnitModel.objects.get(pk=m).get_bed_num,  # текущий коечный фонд
                    # общее количество наблюдаемых на сегодня
                    'curr_log_num': AROLogModel.objects.filter(
                        reg_datetime__gte=timezone.now().date() + timedelta(hours=DELTA),
                        mo_unit=m
                    ).count(),
                    # общее количество свободных коек на сегодня
                    'free_bed_num':
                        BedSpaceNumberModel.objects.filter(mo_unit=m).latest().num
                        -
                        AROLogModel.objects.filter(
                        reg_datetime__gte=timezone.now().date() + timedelta(hours=DELTA),
                        mo_unit=m
                        ).count()
                        +
                        AROLogModel.objects.filter(
                        reg_datetime__gte=timezone.now().date() + timedelta(hours=DELTA),
                        s_dyn='5',  # летальные
                        mo_unit=m
                        ).count(),
                    #
                    # количество поступлений на сегодня
                    'curr_new_num': AROLogModel.objects.filter(
                        reg_datetime__gte=timezone.now().date() + timedelta(hours=DELTA),
                        s_dyn='1',
                        mo_unit=m
                    ).count(),
                    #
                    # # Количество ухудшений состояний на сегодня
                    'curr_decline_num': AROLogModel.objects.filter(
                        reg_datetime__gte=timezone.now().date() + timedelta(hours=DELTA),
                        s_dyn='4',
                        mo_unit=m
                    ).count(),
                    #
                    # # количество летальных на сегодня
                    'curr_lethal_num': AROLogModel.objects.filter(
                        reg_datetime__gte=timezone.now().date() + timedelta(hours=DELTA),
                        s_dyn='5',
                        mo_unit=m
                    ).count()

                }
                mou_list.append(mou)
            context['total_bed_num'] = total_bed_num
            context['total_free_bed_num'] = total_free_bed_num
            context['today_mou_list'] = mou_list

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
            reg_datetime__gte=timezone.now().date() + timedelta(hours=DELTA)
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
                reg_datetime__gte=timezone.now().date() + timedelta(hours=DELTA)
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
            ).distinct().order_by('-reg_datetime')
        else:
            object_list = AROLogModel.objects.filter(
                mh_num__icontains=query
            ).distinct().order_by('mo_unit', '-reg_datetime')

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
