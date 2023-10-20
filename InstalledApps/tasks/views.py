from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from .forms import TaskForm
from .forms import Task

# Create your views here.


def home(request):
    title = 'Hola mundo '
    return render(request, 'home.html')


def tasks(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'tasks.html', {
        'tasks': tasks,
        'title': 'Pending tasks'
    })


@login_required
def task_completed(request):
    tasks = Task.objects.filter(
        user=request.user, date_completed__isnull=False).order_by('date_completed')
    return render(request, 'tasks.html', {
        'tasks': tasks,
        'title': 'Completed tasks'
    })


@login_required
def task_create(request):
    if request.method == 'GET':
        return render(request, 'task_create.html', {
            'form': TaskForm
        })
    elif request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                user_task = form.save(commit=False)
                user_task.user = request.user
                user_task.save()
                return redirect('tasks')
            except ValueError:
                return render(request, 'task_create.html', {
                    'form': TaskForm,
                    'errorform': 'Invalid data'
                })
        else:
            errorform = "<ul>"
            for field, errors in form.errors.items():
                for error in errors:
                    errorform += f"<li>Error in '{field}': {error}</li>"
            errorform += "</ul>"
            return render(request, 'task_create.html', {
                'form': TaskForm,
                "errorform": errorform
            })


@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    elif request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            try:
                form.save()
                return render(request, 'task_detail.html', {
                    'task': task,
                    'form': form
                })
            except ValueError:
                return render(request, 'task_detail.html', {
                    'task': task,
                    'form': form,
                    'errorform': "Error updating task"
                })
        else:
            errorform = "<ul>"
            for field, errors in form.errors.items():
                for error in errors:
                    errorform += f"<li>Error in '{field}': {error}</li>"
            errorform += "</ul>"
            return render(request, 'task_detail.html', {
                'form': form,
                "errorform": errorform
            })


@login_required
def task_complete(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            try:
                task.date_completed = timezone.now()
                task.save()
                return redirect('tasks')
            except ValueError:
                return render(request, 'task_detail.html', {
                    'task': task,
                    'form': form,
                    'errorform': "Error completing task"
                })
        else:
            errorform = "<ul>"
            for field, errors in form.errors.items():
                for error in errors:
                    errorform += f"<li>Error in '{field}': {error}</li>"
            errorform += "</ul>"
            return render(request, 'task_detail.html', {
                'form': form,
                "errorform": errorform
            })


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
