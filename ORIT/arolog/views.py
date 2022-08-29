from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from .models import AROLogModel


class Home(generic.ListView):
    template_name = 'arolog/home.html'
    context_object_name = 'latest_rec_list'
    # paginate_by = 25

    def get_queryset(self):
        """ возвращает последние 10 записей """
        return AROLogModel.objects.order_by('-edit_datetime')[:10]


class AListView(generic.ListView):

    def get_queryset(self):
        return AROLogModel.objects.order_by('-edit_datetime')


#@method_decorator(login_required, name='dispatch')
class ADetailView(generic.DetailView):
    model = AROLogModel
    template_name = 'arolog/arolog_detail.html'

class SearchResultsView(generic.ListView):
    model = AROLogModel
    paginate_by = 25
    template_name = 'arolog/search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = AROLogModel.objects.filter(
            mh_num__icontains=query # поиск по номеру истории болезни
        ).distinct()
        return object_list
