from django.urls import path
from .views import HomePageView, ListCreateView, ListDetailView, ListUpdateView, ListDeleteView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskCompleteView, TaskAllView, ClassCreateView, ClassAllView, ClassUpdateView, ClassDeleteView, SettingsView

urlpatterns = [
    path('', HomePageView, name='home'),
    path('settings', SettingsView, name='settings'),
    path('list/new', ListCreateView, name='list_new'),
    path('list/<uuid:pk>/', ListDetailView, name='list_detail'),
    path('list/<uuid:pk>/update', ListUpdateView, name='list_update'),
    path('list/<uuid:pk>/delete', ListDeleteView, name='list_delete'),
    path('task/<uuid:pk>/new', TaskCreateView, name='task_new'),
    path('task/<uuid:pk>/update', TaskUpdateView, name='task_update'),
    path('task/<uuid:pk>/delete', TaskDeleteView, name='task_delete'),
    path('task/<uuid:task_id>/<str:complete>/complete', TaskCompleteView, name='task_complete'),
    path('task/all', TaskAllView, name='task_all'),
    path('class/new', ClassCreateView, name='class_new'),
    path('class/all', ClassAllView, name='class_all'),
    path('class/<uuid:pk>/update', ClassUpdateView, name='class_update'),
    path('class/<uuid:pk>/delete', ClassDeleteView, name='class_delete'),
]