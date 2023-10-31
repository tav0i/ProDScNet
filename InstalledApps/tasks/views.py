from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from .forms import Task, TaskForm
from .serializers import TaskSerializer

import json
import requests
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from InstalledApps.general.constants import Constants


# REST tasks
@permission_classes([IsAuthenticated])
@login_required
def tasks(request, is_not_completed):
    context = {}
    if is_not_completed == 'False':
        is_not_completed = False
        context.update({
            Constants.FORM_TITLE: 'Completed Task',
            Constants.FORM_ACTION: '/task/False'
        })
    else:
        is_not_completed = True
        context.update({
            Constants.FORM_TITLE: 'Pending Task',
            Constants.FORM_ACTION: '/task/True'
        })
    tasks = Task.objects.filter(
        user=request.user,
        date_completed__isnull=is_not_completed).order_by('date_completed')
    context.update({
        'tasks': tasks,
    })
    
    rest_url = f'{settings.API_BASE_URL}api/tasks/{is_not_completed}/'
    access_token = str(request.session.get(Constants.ACCESS_TOKEN))
    headers = {Constants.AUTHORIZATION: f'{Constants.AUTORIZATION_TYPE} {access_token}'}
    data = {}
    try:
        response = requests.get(rest_url, headers=headers, data=data)
        if response.status_code == 200:
            task_rest_data = response.json()
            tasks_serializer = TaskSerializer(data=task_rest_data)
            print(f'REST: {task_rest_data}')
            print(f'SERIALIZADOS: {tasks_serializer}')
            print(f'ES VALIDO: {tasks_serializer.is_valid()}')
            # if tasks_serializer.is_valid():
            #     print('es valido')
            # else:
            #    print(f'messsages: {tasks_serializer.error_messages}')
            #   context.update({
            #       Constants.ERROR_FORM: tasks_serializer.error_messages
            #   })
    except Exception as e:
        context.update({
            Constants.ERROR_FORM: {Constants.ERROR_SET: e}
            })
    return render(request, 'tasks.html', context)


@login_required
def task_create(request):
    context = {
        Constants.FORM: TaskForm,
        Constants.FORM_ACTION: '/task/create/'
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
                context.update({Constants.ERROR_FORM: {Constants.ERROR_SET: 'Invalid data'}})
                return render(request, 'task_create.html', context)
        else:
            context.update({Constants.ERROR_FORM: form.errors.items()})
            return render(request, 'task_create.html', context)

@permission_classes([IsAuthenticated])
@login_required

def task_detail(request, task_id):
    context = {
        Constants.FORM_ACTION: f"/task/{task_id}/",
    }
    task = get_object_or_404(
        Task,
        pk=task_id,
        user=request.user
    )
    rest_url = f'{settings.API_BASE_URL}api/task/{task_id}/'
    access_token = str(request.session.get(Constants.ACCESS_TOKEN))
    headers = {Constants.AUTHORIZATION: f'{Constants.AUTORIZATION_TYPE} {access_token}'}
    data = {}
    
    try:
        response = requests.get(rest_url, headers=headers, data=data)
        if response.status_code == 200:
            task_rest_data = response.json()
            tasks_serializer = TaskSerializer(data=task_rest_data)
            print(f'REST: {task_rest_data}')
            print(f'SERIALIZADOS: {tasks_serializer}')
            print(f'ES VALIDO: {tasks_serializer.is_valid()}')
            # if tasks_serializer.is_valid():
            #     print('es valido')
            # else: 
            #     print(f'messsages: {tasks_serializer.error_messages}')
            #     context.update({
            #         Constants.ERROR_FORM: tasks_serializer.error_messages
            #     })
    except Exception as e:
        context.update({
            Constants.ERROR_FORM: {Constants.ERROR_SET: e}
            })
    if request.method == 'GET':
        form = TaskForm(instance=task)
        context.update({
            Constants.FORM: form,
            'task': task,
        })
        return render(request, 'task_detail.html', context)
    elif request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        context.update({Constants.FORM: form})
        if form.is_valid():
            try:
                form.save()
                context.update({'task': task, })
                return render(request, 'task_detail.html', context)
            except ValueError:
                context.update({
                    'task': task,
                    Constants.ERROR_FORM: {Constants.ERROR_SET: 'Error updating task'}
                })
                return render(request, 'task_detail.html', context)
        else:
            context.update({Constants.ERROR_FORM: form.errors.items()})
            return render(request, 'task_detail.html', context)


@login_required
def task_complete(request, task_id):
    context = {
        Constants.FORM_ACTION: f"/task/{task_id}/",
    }
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(request.POST, instance=task)
        context.update({Constants.FORM: form})
        if form.is_valid():
            try:
                task.date_completed = timezone.now()
                task.save()
                return redirect(reverse('tasks', args=['True']))
            except ValueError:
                context.update({
                    'task': task,
                    Constants.ERROR_FORM: {Constants.ERROR_SET: 'Error completing task'}
                })
                return render(request, 'task.html', context)
        else:
            context.update({Constants.ERROR_FORM: form.errors.items()})
            return render(request, 'task.html', context)


@login_required
def task_delete(request, task_id):
    context = {
        Constants.FORM_ACTION: f"/task/{task_id}/",
    }
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(request.POST, instance=task)
        context.update({Constants.FORM: form})
        if form.is_valid():
            try:
                task.delete()
                if task.date_completed == None:
                    return redirect(reverse('tasks', args=['True']))
                else:
                    return redirect(reverse('tasks', args=['False']))
            except ValueError:
                context.update({
                    'task': task,
                    Constants.ERROR_FORM: {Constants.ERROR_SET: 'Error deleting task'}
                })
                return render(request, 'task.html', context)
        else:
            context.update({Constants.ERROR_FORM: form.errors.items()})
            return render(request, 'task.html', context)
