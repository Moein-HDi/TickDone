from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

@login_required(login_url='login')
def HomePageView(request):
    Lists = TodoList.objects.filter(owner=request.user)
    context = {
        'Lists': Lists,
    }
    return render(request, 'home.html', context)

@login_required(login_url='login')
def NewListView(request):
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
    

