from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from django.conf import settings
from .forms import TaskForm
from .forms import Task

# Create your views here.


def home(request):
    gretting = 'Saludos desde el programa de django'
    return render(request, 'home.html', {
        'gretting':gretting,
        'STATIC_URL_': settings.STATIC_URL,
        'MEDIA_ROOT_': settings.MEDIA_ROOT,
        'MEDIA_URL_': settings.MEDIA_URL,
        'BASE_DIR_': settings.BASE_DIR,
    })


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
        print('pending')
        context.update({'title':'Pending Task'})
        context.update({'formaction': '/task/True'})
    else:
        print('complete')
        context.update({'title':'Completed Task'})
        context.update({'formaction': '/task/False'})
    
    return render(request, 'tasks.html', context)


@login_required
def task_create(request):
    if request.method == 'GET':
        return render(request, 'task_create.html', {
            'form': TaskForm,
            'formaction': '/task/create/'
        })
    elif request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                user_task = form.save(commit=False)
                user_task.user = request.user
                user_task.save()
                return redirect('tasks/True')
            except ValueError:
                return render(request, 'task_create.html', {
                    'form': TaskForm,
                    'errorform': 'Invalid data',
                    'formaction': '/task/create/'
                })
        else:
            return render(request, 'task_create.html', {
                'form': TaskForm,
                'formaction': '/task/create/',
                "errorform": form.errors.items(),
            })


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form,
            'formaction': f"/task/{task_id}/",
        })
    elif request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            try:
                form.save()
                return render(request, 'task_detail.html', {
                    'task': task,
                    'form': form,
                    'formaction': f"/task/{task_id}/",
                })
            except ValueError:
                return render(request, 'task_detail.html', {
                    'task': task,
                    'form': form,
                    'formaction': f"/task/{task_id}/",
                    'errorform': "Error updating task"
                })
        else:
            return render(request, 'task_detail.html', {
                'form': form,
                'formaction': f"/task/'{task_id}/",
                'errorform': form.errors.items(),
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
                return render(request, 'task.html', {
                    'task': task,
                    'form': form,
                    'formaction': f"/task/'{task_id}/",
                    'errorform': "Error completing task"
                })
        else:
            return render(request, 'task.html', {
                'form': form,
                'formaction': f"/task/'{task_id}/",
                "errorform": form.errors.items(),
            })


@login_required
def task_delete(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            try:
                task.delete()
                return redirect('tasks/True')
            except ValueError:
                return render(request, 'task.html', {
                    'task': task,
                    'form': form,
                    'formaction': f"/task/'{task_id}/",
                    'errorform': "Error deleting task"
                })
        else:
            return render(request, 'task.html', {
                'form': form,
                'formaction': f"/task/'{task_id}/",
                "errorform": form.errors.items(),
            })
