from django.shortcuts import render

from .models import Task


def index(request):
    context = {
        'tasks': Task.objects.all()
    }
    return render(request, 'tasks/index.html', context=context)