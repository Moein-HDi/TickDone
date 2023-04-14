from django.urls import path
from .views import HomePageView, NewListView

urlpatterns = [
    path('', HomePageView, name='home'),
    path('list_new', NewListView, name='list_new'),
    
]