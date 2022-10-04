from django.urls import path

from .views import BedSpaceCreateView, MOUnitModelListView, MOUitDetailView

urlpatterns = [
    path('', MOUnitModelListView.as_view(), name='mou_list'),
    path('bed/add/', BedSpaceCreateView.as_view(), name='bed_add'),
    path('<int:pk>/', MOUitDetailView.as_view(), name='mou_detail'),
]
