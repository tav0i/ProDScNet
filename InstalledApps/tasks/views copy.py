from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from .forms import TaskForm
from .forms import Task

import requests
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.authentication import JWTAuthentication

# REST tasks
@authentication_classes([JWTAuthentication])  # Utiliza JWTAuthentication para autenticación
@permission_classes([IsAuthenticated])  # Requiere autenticación
@login_required
def tasks(request, is_not_completed):
    context = {}
    if is_not_completed == 'True':
        context.update({
            'title': 'Pending Task',
            'formaction': '/task/True'
            })
    else:
        context.update({
            'title': 'Completed Task',
            'formaction': '/task/False'
            })
    try:
        rest_url = f'{settings.API_BASE_URL}api/tasks/{is_not_completed}'
        access_token = request.session.get('access_token')
        headers = {'Authorization': {access_token}}
        response = requests.get(rest_url, headers)
        print(f'se ejecuta la consulta {response}')
        print(context)
        if response.status_code == 200:
            rest_data = response.json()
            tasks = TaskSerializer(data=rest_data, many=True)
            print(tasks)
            if serializer.is_valid():
                tasks = serializer.save()
        context.update({
            'tasks': tasks, 
        })
    except Exception as e:
        context.update({
            'errorform': {'errorset': e}
            })
        return render(request, 'tasks.html', context)
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
                data = form.cleaned_data
                response = requests.post('api/task/create', data=data)
                
                #user_task = form.save(commit=False)
                #user_task.user = request.user
                #user_task.save()

                if response.status_code == 201:
                    return redirect(reverse('tasks', args=['True']))
                else:
                    context.update({'errorform': {'errorset': 'Create API Fail'}})
                    return render(request, 'task_create.html', context)
            except requests.exceptions.RequestException as e:
                context.update({'errorform': {'errorset': e}})
                return render(request, 'task_create.html', context)
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
                if task.date_completed == None:
                    return redirect(reverse('tasks', args=['True']))
                else:
                    return redirect(reverse('tasks', args=['False']))
            except ValueError:
                context.update({
                    'task': task,
                    'errorform': {'errorset': 'Error deleting task'}
                    })
                return render(request, 'task.html', context)
        else:
            context.update({'errorform': form.errors.items()})
            return render(request, 'task.html', context)
