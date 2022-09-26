import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from .models import AROLogModel
from mo.models import StaffModel, BedSpaceNumberModel


def index(request):
    context = {'title': 'Добро пожаловать!'}
    return render(request, 'arolog/welcome.html', context)


@method_decorator(login_required, name='dispatch')
class Home(generic.ListView):
    template_name = 'arolog/home.html'

    def get_queryset(self):
        # Тут добавить возврат записей в зависимости от роли пользователя (все или только свои)
        #
        if StaffModel.objects.get(user=self.request.user).is_unit_only:
            q = Q(
                registrator__user=self.request.user
            ) & Q(
                reg_datetime__date=datetime.datetime.today().date()
            )
            return AROLogModel.objects.filter(q).order_by('-edit_datetime')
        else:
            q = Q(
                reg_datetime__date=datetime.datetime.today().date()
            )
            return AROLogModel.objects.filter(q).order_by('mo_unit', '-edit_datetime')

    # вернуть наименование подразделения зарегистриованного пользователя, его коечный фонд, количество св.коек
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['staff'] = StaffModel.objects.get(user=self.request.user)  # contains title, fio, mo & mo_unit fields
        mou = context['staff'].mo_unit

        # Коечный фонд своего отделения
        #
        '''
        кол-во занятых коек отделения текущего пользователя равно 
        кол-ву сегодняшних записей для отделения текущего пользователя
        '''
        if mou:
            occ_bed_num = AROLogModel.objects.filter(
                mo_unit=mou,
                reg_datetime__date=datetime.datetime.now().date()
            ).count()
            context['occ_bed_num'] = occ_bed_num
            if BedSpaceNumberModel.objects.filter(mo_unit=mou):
                context['bed_num'] = BedSpaceNumberModel.objects.filter(mo_unit=mou).latest().num
                context['free_bed_num'] = context['bed_num'] - occ_bed_num
                context['free_bed_percent'] = round(context['free_bed_num'] / context['bed_num'] * 100, 1)
            else:
                context['bed_num'] = 'нет данных'
                context['free_bed_num'] = 'нет данных'
                context['free_bed_percent'] = '-'

        return context


@method_decorator(login_required, name='dispatch')
class AListView(generic.ListView):
    paginate_by = 10

    def get_queryset(self):
        q = Q(
            reg_datetime__date=datetime.datetime.today().date()
        )
        return AROLogModel.objects.filter(q).order_by('-edit_datetime')


@method_decorator(login_required, name='dispatch')
class ADetailView(generic.DetailView):
    model = AROLogModel
    template_name = 'arolog/arolog_detail.html'


@method_decorator(login_required, name='dispatch')
class SearchResultsView(generic.ListView):
    model = AROLogModel
    paginate_by = 25
    template_name = 'arolog/search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = AROLogModel.objects.filter(
            mh_num__icontains=query  # поиск по номеру истории болезни
        ).distinct()
        return object_list


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

    def form_valid(self, form):
        form.instance.mo = StaffModel.objects.get(user=self.request.user).mo
        form.instance.mo_unit = StaffModel.objects.get(user=self.request.user).mo_unit
        form.instance.registrator = StaffModel.objects.get(user=self.request.user)

        return super().form_valid(form)
