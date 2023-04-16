from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *


# Homepage
@login_required(login_url='login')
def HomePageView(request):
    Lists = TodoList.objects.filter(owner=request.user)
    context = {
        'Lists': Lists,
    }
    return render(request, 'home.html', context)

# list - new
@login_required(login_url='login')
def ListCreateView(request):
    if request.method == "POST":
        name = request.POST.get('name')
        newlist = TodoList.objects.create(name=name, owner=request.user)
        newlist.save()
        return redirect('/')
    else:
        Lists = TodoList.objects.filter(owner=request.user)
        context = {
            'Lists': Lists,
        }
        return render(request, 'list_new.html', context)
    
# list - detail
@login_required(login_url='login')
def ListDetailView(request, pk):
    Lists = TodoList.objects.filter(owner=request.user)

    current_list = get_object_or_404(TodoList, pk=pk)
    Tasks = TodoItem.objects.filter(todo_list=current_list)
    
    context = {
        'Lists': Lists,
        'current_list': current_list,
        'Tasks': Tasks,
    }
    return render(request, 'list_detail.html', context)

#list - update
@login_required(login_url='login')
def ListUpdateView(request, pk):
    if request.method == "POST":
        name = request.POST.get('name')
        current_list = get_object_or_404(TodoList, pk=pk)
        current_list.name = name
        current_list.save()
        return redirect('/')
    else:
        Lists = TodoList.objects.filter(owner=request.user)
        current_list = get_object_or_404(TodoList, pk=pk)
        context = {
            'Lists': Lists,
            'current_list': current_list
        }
        return render(request, 'list_update.html', context)
    
#list - delete
@login_required(login_url='login')
def ListDeleteView(request, pk):
    if request.method == "POST":
        
        current_list = get_object_or_404(TodoList, pk=pk)
        current_list.delete()
        return redirect('/')
    else:
        Lists = TodoList.objects.filter(owner=request.user)
        current_list = get_object_or_404(TodoList, pk=pk)
        context = {
            'Lists': Lists,
            'current_list': current_list,
        }
        return render(request, 'list_delete.html', context)