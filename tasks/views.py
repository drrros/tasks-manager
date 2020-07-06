import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required  # , permission_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import TaskForm
from .models import Task
from .filters import TaskFilter


@login_required(login_url='login_user')
def index(request):
    author = User.objects.get(username=request.user.username)
    tasks = Task.objects.filter(author_id=author.id).filter(
        task_date__gte=(timezone.localtime() - datetime.timedelta(days=7))).order_by(
        'task_date')
    task_filter = TaskFilter(request.GET, queryset=tasks)
    tasks = task_filter.qs
    context = {
        'tasks': tasks,
        'task_filter': task_filter
    }
    return render(request, 'tasks/index.html', context=context)


@login_required(login_url='login_user')
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.author = User.objects.get(username=request.user.username)
            form.save()
            return redirect('index')
    else:
        form = TaskForm()
    context = {'form': form, 'type': 'create'}
    return render(request, 'tasks/task_form.html', context)


@login_required(login_url='login_user')
def update_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form': form, 'type': 'update'}
    return render(request, 'tasks/task_form.html', context)


@login_required(login_url='login_user')
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.method == 'GET':
        if task.author_id == request.user.id:
            task.delete()
            return redirect('index')
    context = {'item': task}
    return render(request, 'tasks/delete_task.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(password=password, username=username)
            if user:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Неправильное имя пользователя или пароль')
        return render(request, 'tasks/login.html', context={})


@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    return redirect('login_user')
