from django.shortcuts import render, get_object_or_404, redirect

from .forms import TaskForm
from .models import Task


def index(request):
    context = {
        'tasks': Task.objects.all()
    }
    return render(request, 'tasks/index.html', context=context)


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = TaskForm()
    context = {'form': form, 'type': 'create'}
    return render(request, 'tasks/task_form.html', context)


def update_task(request):
    return None


def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('index')
    context = {'item': task}
    return render(request, 'tasks/delete_task.html', context)