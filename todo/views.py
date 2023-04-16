from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.urls import reverse

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
        next = request.GET.get('next', reverse('home'))
        return HttpResponseRedirect(next)
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
    
# task - new
@login_required(login_url='login')
def TaskCreateView(request, pk):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        
        current_list = get_object_or_404(TodoList, pk=pk)
        if due_date != '':
            newtask = TodoItem.objects.create(name=name, description=description, due_date=due_date, todo_list=current_list)
        else:
            newtask = TodoItem.objects.create(name=name, description=description, todo_list=current_list)
        newtask.save()
        next = request.GET.get('next', reverse('home'))
        return HttpResponseRedirect(next)

    else:
        Lists = TodoList.objects.filter(owner=request.user)
        current_list = get_object_or_404(TodoList, pk=pk)
        context = {
            'Lists': Lists,
            'current_list': current_list,
        }
        return render(request, 'task_new.html', context)
    
# task - update
@login_required(login_url='login')
def TaskUpdateView(request, pk):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')

        current_task = get_object_or_404(TodoItem, pk=pk)
        current_task.name = name
        current_task.due_date = due_date
        current_task.description = description
        current_task.save()
        next = request.GET.get('next', reverse('home'))
        return HttpResponseRedirect(next)
    else:
        Lists = TodoList.objects.filter(owner=request.user)
        current_task = get_object_or_404(TodoItem, pk=pk)
        context = {
            'Lists': Lists,
            'current_task': current_task
        }
        return render(request, 'task_update.html', context)