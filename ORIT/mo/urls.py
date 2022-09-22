from django.urls import path

from .views import BedSpaceCreateView

urlpatterns = [
    # path('search/', SearchResultsView.as_view(), name='search_results'),
    # path('bed/', MOListView.as_view(), name='list'),
    path('bed/add/', BedSpaceCreateView.as_view(), name='create'),
    # path('arolog/<int:pk>/', ADetailView.as_view(), name='detail'),
    # path('', Home.as_view(), name='home')
]
