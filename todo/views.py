from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.urls import reverse
from django.http import JsonResponse
import jdatetime, datetime


# Homepage
@login_required(login_url='login')
def HomePageView(request):
    
    if datetime.datetime.now().hour >= 0 and datetime.datetime.now().hour <= 12:
        greeting = 'صبح بخیر🌅'
    elif datetime.datetime.now().hour > 12 and datetime.datetime.now().hour <= 18:
        greeting = 'عصر بخیر☕'
    elif datetime.datetime.now().hour > 18 and datetime.datetime.now().hour < 24:
        greeting = 'شب بخیر🌙'
    date = jdatetime.date.today().strftime("%A %d %B %Y")
    today = jdatetime.date.today()
    tomorrow_date = today + jdatetime.timedelta(days=1)
    today_weekday = jdatetime.date.today().strftime("%A")
    Lists = TodoList.objects.filter(owner=request.user)

    Classes = ClassItem.objects.filter(owner=request.user, weekday=today_weekday)
    Tasks = TodoItem.objects.filter(due_date=tomorrow_date, todo_list__in=Lists)
    
    context = {
        'Lists': Lists,
        'date': date,
        'Tasks': Tasks,
        'Classes': Classes,
        'greeting': greeting,
    }
    return render(request, 'home.html', context)

# settings
@login_required(login_url='login')
def SettingsView(request):
    Lists = TodoList.objects.filter(owner=request.user)
    date_joined = jdatetime.date.fromgregorian(date=request.user.date_joined).strftime("%A %d %B %Y")
    context = {
        'Lists': Lists,
        'date_joined': date_joined,
    }
    return render(request, 'settings.html', context)

# list - new
@login_required(login_url='login')
def ListCreateView(request):
    if request.method == "POST":
        if TodoList.objects.filter(owner=request.user).count() < 10:
            name = request.POST.get('name')
            newlist = TodoList.objects.create(name=name, owner=request.user)
            newlist.save()
            return redirect('/')
        else:
            Lists = TodoList.objects.filter(owner=request.user)
            context = {
                'Lists': Lists,
            }
            return render(request, 'list_new_error.html', context)
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
    Tasks = Tasks.order_by('due_date')
    NotDoneTasks = []
    DoneTasks = []
    NoDateTasks = []
    for task in Tasks:    
        if task.due_date:
            today = jdatetime.date.today()
            due = jdatetime.date(task.due_date.year, task.due_date.month, task.due_date.day)
            days = due - today
            task.due_date = days.days

        if task.completed == False and task.due_date:
            NotDoneTasks.append(task)
        if task.completed == True:
            DoneTasks.append(task)
        if task.completed == False and not task.due_date:
            # task.due_date = "null"
            NoDateTasks.append(task)
            
            
    context = {
        'Lists': Lists,
        'current_list': current_list,
        'Tasks': NotDoneTasks,
        'DoneTasks': DoneTasks,
        'NoDateTasks': NoDateTasks
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
        if due_date != '':
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
    
#task - delete
@login_required(login_url='login')
def TaskDeleteView(request, pk):
    if request.method == "POST":
        
        current_task = get_object_or_404(TodoItem, pk=pk)
        current_task.delete()
        return redirect('/')
    else:
        Lists = TodoList.objects.filter(owner=request.user)
        current_task = get_object_or_404(TodoItem, pk=pk)
        context = {
            'Lists': Lists,
            'current_task': current_task
        }
        return render(request, 'task_delete.html', context)

# task - complete
@login_required(login_url='login')
def TaskCompleteView(request, task_id, complete):
    task = get_object_or_404(TodoItem, pk=task_id)
    if complete == 'true':
        task.completed = True
    if complete == 'false':
        task.completed = False
    task.save()
    return JsonResponse({'status': 'success', 'message': 'Task updated successfully.'})


# task - all
@login_required(login_url='login')
def TaskAllView(request):
    Lists = TodoList.objects.filter(owner=request.user)
    Tasks = TodoItem.objects.filter(todo_list__in=Lists)
    Tasks = Tasks.order_by('due_date')
    NotDoneTasks = []
    DoneTasks = []
    NoDateTasks = []
    for task in Tasks:    
        if task.due_date:
            today = jdatetime.date.today()
            due = jdatetime.date(task.due_date.year, task.due_date.month, task.due_date.day)
            days = due - today
            task.due_date = days.days

        if task.completed == False and task.due_date:
            NotDoneTasks.append(task)
        if task.completed == True:
            DoneTasks.append(task)
        if task.completed == False and not task.due_date:
            # task.due_date = "null"
            NoDateTasks.append(task)
            
            
    context = {
        'Lists': Lists,
        'Tasks': NotDoneTasks,
        'DoneTasks': DoneTasks,
        'NoDateTasks': NoDateTasks
    }
    return render(request, 'task_all.html', context)

# class - new
@login_required(login_url='login')
def ClassCreateView(request):
    if request.method == "POST":
        name = request.POST.get('name')
        time_start = request.POST.get('time_start')
        time_end = request.POST.get('time_end')
        weekday = request.POST.get('weekday')
        location = request.POST.get('location')
        newClass = ClassItem.objects.create(name=name, time_start=time_start, time_end=time_end, weekday=weekday, location=location, owner=request.user)
        newClass.save()
        return redirect('/')
    else:
        Lists = TodoList.objects.filter(owner=request.user)
        context = {
            'Lists': Lists,
        }
    return render(request, 'class_new.html', context)

# class - all
@login_required(login_url='login')
def ClassAllView(request):

    Lists = TodoList.objects.filter(owner=request.user)
    Classes = ClassItem.objects.filter(owner=request.user)
    Classes = Classes.order_by('time_start')
    AllWeekdays = [
        'Saturday',
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday'
    ]
    weekdays = [classitem.weekday for classitem in Classes]
    AllWeekdays = [weekday for weekday in AllWeekdays if weekday in weekdays]
               
    
    context = {
        'Lists': Lists,
        'Classes': Classes,
        'Weekdays': AllWeekdays,
    }
    return render(request, 'class_all.html', context)

# class - update
@login_required(login_url='login')
def ClassUpdateView(request, pk):
    if request.method == "POST":
        name = request.POST.get('name')
        time_start = request.POST.get('time_start')
        time_end = request.POST.get('time_end')
        weekday = request.POST.get('weekday')
        location = request.POST.get('location')


        current_class = get_object_or_404(ClassItem, pk=pk)
        current_class.name = name
        current_class.time_end = time_end
        current_class.time_start = time_start
        current_class.weekday = weekday
        current_class.location = location

        current_class.save()
        next = request.GET.get('next', reverse('home'))
        return HttpResponseRedirect(next)
    else:
        Lists = TodoList.objects.filter(owner=request.user)
        current_class = get_object_or_404(ClassItem, pk=pk)
        context = {
            'Lists': Lists,
            'current_class': current_class
        }
        return render(request, 'class_update.html', context)
    
#task - delete
@login_required(login_url='login')
def ClassDeleteView(request, pk):
    if request.method == "POST":
        
        current_class = get_object_or_404(ClassItem, pk=pk)
        current_class.delete()
        return redirect('/')
    else:
        Lists = TodoList.objects.filter(owner=request.user)
        current_class = get_object_or_404(ClassItem, pk=pk)
        context = {
            'Lists': Lists,
            'current_class': current_class
        }
        return render(request, 'class_delete.html', context)
