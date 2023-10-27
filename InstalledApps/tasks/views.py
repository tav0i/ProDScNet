from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from .forms import TaskForm
from .forms import Task

# Create your views here.


def home(request):
    gretting = 'Saludos desde el programa de django'
    context = {
        'gretting': gretting,
        'STATIC_URL_': settings.STATIC_URL,
        'MEDIA_ROOT_': settings.MEDIA_ROOT,
        'MEDIA_URL_': settings.MEDIA_URL,
        'BASE_DIR_': settings.BASE_DIR,
    }
    return render(request, 'home.html', context)


@login_required
def tasks(request, is_not_completed):
    if is_not_completed == 'True':
        is_not_completed = True
    else:
        is_not_completed = False
    tasks = Task.objects.filter(
        user=request.user,
        date_completed__isnull=is_not_completed).order_by('date_completed')

    context = {
        'tasks': tasks,
    }
    if is_not_completed:
        context.update({
            'title': 'Pending Task',
            'formaction': '/task/True'
            })
    else:
        context.update({
            'title': 'Completed Task',
            'formaction': '/task/False'
            })

    return render(request, 'tasks.html', context)


@login_required
def task_create(request):
    context = {
        'form': TaskForm,
        'formaction': '/task/create/'
    }
    if request.method == 'GET':
        return render(request, 'task_create.html', context)
    elif request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                user_task = form.save(commit=False)
                user_task.user = request.user
                user_task.save()
                return redirect(reverse('tasks', args=['True']))
            except ValueError:
                context.update({'errorform': {'errorset': 'Invalid data'}})
                return render(request, 'task_create.html', context)
        else:
            context.update({'errorform': form.errors.items()})
            return render(request, 'task_create.html', context)


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    context = {
        'formaction': f"/task/{task_id}/",
    }
    if request.method == 'GET':
        form = TaskForm(instance=task)
        context.update({
            'form': form,
            'task': task,
            })
        return render(request, 'task_detail.html', context)
    elif request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        context.update({'form': form})
        if form.is_valid():
            try:
                form.save()
                context.update({'task': task,})
                return render(request, 'task_detail.html', context)
            except ValueError:
                context.update({
                    'task': task,
                    'errorform': {'errorset': 'Error updating task'}
                    })
                return render(request, 'task_detail.html', context)
        else:
            context.update({'errorform': form.errors.items()})
            return render(request, 'task_detail.html', context)


@login_required
def task_complete(request, task_id):
    context = {
        'formaction': f"/task/{task_id}/",
    }
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(request.POST, instance=task)
        context.update({'form': form})
        if form.is_valid():
            try:
                task.date_completed = timezone.now()
                task.save()
                return redirect(reverse('tasks', args=['True']))
            except ValueError:
                context.update({
                    'task': task,
                    'errorform': {'errorset': 'Error completing task'}
                    })
                return render(request, 'task.html', context)
        else:
            context.update({'errorform': form.errors.items()})
            return render(request, 'task.html', context)


@login_required
def task_delete(request, task_id):
    context = {
        'formaction': f"/task/{task_id}/",
    }
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(request.POST, instance=task)
        context.update({'form': form})
        if form.is_valid():
            try:
                task.delete()
                return redirect(reverse('tasks', args=['True']))
            except ValueError:
                context.update({
                    'task': task,
                    'errorform': {'errorset': 'Error deleting task'}
                    })
                return render(request, 'task.html', context)
        else:
            context.update({'errorform': form.errors.items()})
            return render(request, 'task.html', context)
