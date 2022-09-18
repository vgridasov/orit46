from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from .models import AROLogModel
from mo.models import *


@method_decorator(login_required, name='dispatch')
class Home(generic.ListView):
    template_name = 'arolog/home.html'
    # context_object_name = 'latest_rec_list'

    # paginate_by = 25

    def get_queryset(self):
        """ возвращает последние 10 записей, в которых в качестве регистратора указан текущий пользователь

        return AROLogModel.objects.order_by('-edit_datetime')[:10]
        """
        q = Q(
            registrator__user=self.request.user
        )
        return AROLogModel.objects.filter(q).order_by('-edit_datetime')[:10]

    # TODO: вернуть наименование подразделения зарегистриованного пользователя, его коечный фонд, количество св.коек
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['mycontext'] = 'Мой контекст'
        context['staff'] = StaffModel.objects.filter(user=self.request.user) # ???
    #     context['mo_unit'] = BedSpaceNumberModel.objects.filter(mo_unit)
    #     context['mo_unit_bed_num'] = BedSpaceNumberModel.objects.filter(mo_unit)
    #     context['mo_unit_free_bed_num'] = BedSpaceNumberModel.objects.filter(mo_unit)
    #
        return context


@method_decorator(login_required, name='dispatch')
class AListView(generic.ListView):
    paginate_by = 25

    def get_queryset(self):
        return AROLogModel.objects.order_by('-edit_datetime')


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
