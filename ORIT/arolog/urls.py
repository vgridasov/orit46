from django.urls import path

from .views import index, Home, AListView, SearchResultsView, ADetailView, ACreateView, AUpdateView

urlpatterns = [
    path('', index, name='home'),
    path('my/', Home.as_view(), name='my'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('arolog/', AListView.as_view(), name='list'),
    path('arolog/add/', ACreateView.as_view(), name='create'),
    path('arolog/<int:pk>/', ADetailView.as_view(), name='detail'),
    path('arolog/<int:pk>/edit/', AUpdateView.as_view(), name='edit')
]
