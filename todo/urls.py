from django.urls import path
from .views import HomePageView, ListCreateView, ListDetailView, ListUpdateView, ListDeleteView, TaskCreateView, TaskUpdateView

urlpatterns = [
    path('', HomePageView, name='home'),
    path('list/new', ListCreateView, name='list_new'),
    path('list/<uuid:pk>/', ListDetailView, name='list_detail'),
    path('list/<uuid:pk>/update', ListUpdateView, name='list_update'),
    path('list/<uuid:pk>/delete', ListDeleteView, name='list_delete'),
    path('task/<uuid:pk>/new', TaskCreateView, name='task_new'),
    path('task/<uuid:pk>/update', TaskUpdateView, name='task_update'),
]