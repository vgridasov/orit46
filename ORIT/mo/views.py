from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from .models import BedSpaceNumberModel, StaffModel


@method_decorator(login_required, name='dispatch')
class BedSpaceNumberListView(generic.ListView):
    paginate_by = 10

    def get_queryset(self):

        return BedSpaceNumberModel.objects.order_by('-edit_date')


class BedSpaceCreateView(LoginRequiredMixin, generic.CreateView):
    model = BedSpaceNumberModel
    template_name = 'arolog/new_rec.html'
    fields = ["num", "note"]
    success_url = '/'

    def form_valid(self, form):
        form.instance.mo = StaffModel.objects.get(user=self.request.user).mo
        form.instance.mo_unit = StaffModel.objects.get(user=self.request.user).mo_unit

        return super().form_valid(form)
