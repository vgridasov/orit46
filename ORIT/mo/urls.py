from django.urls import path

from .views import BedSpaceCreateView, MOUnitModelListView, MOUitDetailView

urlpatterns = [
    path('', MOUnitModelListView.as_view(), name='moulist'),
    path('bed/add/', BedSpaceCreateView.as_view(), name='create'),
    path('<int:pk>/', MOUitDetailView.as_view(), name='moudetail'),
    # path('', Home.as_view(), name='home')
]
