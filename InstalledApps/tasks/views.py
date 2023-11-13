from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from requests.exceptions import HTTPError
from .forms import Task, TaskForm
from .serializers import TaskSerializer  # , TaskDecoder

import json
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException, HTTPError

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status

from InstalledApps.general.constants import Constants
from InstalledApps.general.exception_handlers import ExceptionHandler


# REST tasks
@permission_classes([IsAuthenticated])
@login_required
def tasks(request, is_not_completed):
    context = {}
    messages = []
    try:
        if is_not_completed.lower() == 'false':
            is_not_completed = False
            context.update({
                Constants.FORM_TITLE: Constants.TASK_COMPLETED,
                Constants.FORM_ACTION: '/task/false'
            })
        elif is_not_completed.lower() == 'true':
            is_not_completed = True
            context.update({
                Constants.FORM_TITLE: Constants.TASK_PENDING,
                Constants.FORM_ACTION: '/task/true'
            })
        # region __TEST__ call to de Models directly
        '''
        tasks = Task.objects.filter(
            user=request.user,
            date_completed__isnull=is_not_completed).order_by('date_completed')
        context.update({
            'tasks': tasks,
        })
        tasks_serializer = TaskSerializer(
            instance=tasks, many=True
        )
        print(f'SERIALIZADO_DIRECTO:  {tasks_serializer.data}')
        '''
        # endregion __TEST__
        # region REST
        rest_url = f'{settings.API_BASE_URL}api/tasks/{is_not_completed}/'
        access_token = str(request.session.get(Constants.ACCESS_TOKEN))
        headers = {
            Constants.AUTHORIZATION: f'{Constants.AUTORIZATION_TYPE} {access_token}'
        }
        data = {}
        response = requests.get(rest_url, headers=headers, data=data)
        if response.status_code == status.HTTP_200_OK:
            tasks_api_response = response.json()
            tasks_api_data = response.json()
            context.update({
                'tasks': tasks_api_response,
            })
            # region __TEST__
            '''
            tasks_api_serializer = TaskSerializer(
                instance=tasks_api_response, many=True) # __IMPORTANT__ data instead intance is for validat and create an object
            print(f'SERIALIZED_REST {tasks_api_serializer.data}')
            '''
            # endregion __TEST__
        else:
            response.raise_for_status()  # Raise a exception for HTTP error
        # endregion REST
    except (ConnectionError, Timeout, RequestException, HTTPError) as e:
        # task_api_response.error_messages
        context.update({
            Constants.ERROR_FORM: {
                Constants.ERROR_SET: f'{Constants.ERROR_API} {e}'}
        })
        ExceptionHandler(e).handle()
    except Exception as e:
        context.update({
            Constants.ERROR_FORM: {
                Constants.ERROR_SET: f'{Constants.ERROR_EXCEPTION} {e}'}
        })
    else:
        print(Constants.FORM_ELSE)
    finally:
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
                return redirect(reverse('tasks', args=['true']))
            except ValueError:
                context.update({
                    Constants.ERROR_FORM: {
                        Constants.ERROR_SET: f'{Constants.VALUE_ERROR} Invalid data'}
                })
                raise Constants.VALUE_ERROR
        else:
            context.update({Constants.ERROR_FORM: form.errors.items()})
            return render(request, 'task_create.html', context)


@permission_classes([IsAuthenticated])
@login_required
def task_detail(request, task_id):
    context = {
        Constants.FORM_ACTION: f"/task/{task_id}/",
    }
    messages = []
    try:
        # region __TEST__ call to de Models directly
        '''
        task = get_object_or_404(
            Task,
            pk=task_id,
            user=request.user
        )
        context.update({
            'task': task,
        })
        task_serializer = TaskSerializer(
            instance=task, many=False
        )
        print(f'SERIALIZADO_DIRECTO:  {task_serializer.data}')
        '''
        # endregion __TEST__
        # region REST
        rest_url = f'{settings.API_BASE_URL}api/task/{task_id}/'
        access_token = str(request.session.get(Constants.ACCESS_TOKEN))
        headers = {
            Constants.AUTHORIZATION: f'{Constants.AUTORIZATION_TYPE} {access_token}'
        }
        data = {}
        response = requests.get(rest_url, headers=headers, data=data)
        if response.status_code == status.HTTP_200_OK:
            task_api_response = response.json()
            context.update({
                'task': task_api_response,
            })
            # region __TEST__
            '''
            task_api_serializer = TaskSerializer(
                instance=task_api_response, many=False # __IMPORTANT__ data instead intance is for validat and create an object
            )
            print(f'SERIALIZED_REST:  {task_api_serializer.data}')
            '''
            # endregion __TEST__
            form = TaskForm(data=task_api_response)
            context.update({
                Constants.FORM: form,
            })
        else:
            context = {
                Constants.FORM: TaskForm,
            }
            response.raise_for_status()  # Raise a exception for HTTP error
        # endregion REST
    except (ConnectionError, Timeout, RequestException, HTTPError) as e:
        # task_api_response.error_messages
        print(f'Exception INSIDE DETAIL  {e}')
        context.update({
            Constants.ERROR_FORM: {
                Constants.ERROR_SET: f'{Constants.ERROR_API} {e}'}
        })
        # ExceptionHandler(e).handle()
    except Exception as e:
        print(f'Exception {e}')
        context.update({
            Constants.ERROR_FORM: {
                Constants.ERROR_SET: f'{Constants.ERROR_EXCEPTION} {e}'}
        })
    else:
        print(Constants.FORM_ELSE)
    finally:
        return render(request, 'task_detail.html', context)
    '''
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
                    Constants.ERROR_FORM: {
                        Constants.ERROR_SET: f'{Constants.VALUE_ERROR} Error updating book'}
                })
                raise Constants.VALUE_ERROR
        else:
            context.update({
                Constants.ERROR_FORM: form.errors.items()
            })
            raise Constants.ERROR_CUSTOM
            return render(request, 'task_detail.html', context)
    '''


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
                    Constants.ERROR_FORM: {Constants.ERROR_SET: f'{Constants.VALUE_ERROR} Error completing book'},
                })
                raise Constants.VALUE_ERROR
        else:
            context.update({
                Constants.ERROR_FORM: form.errors.items()
            })
            raise Constants.ERROR_CUSTOM
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
                    return redirect(reverse('tasks', args=['true']))
                else:
                    return redirect(reverse('tasks', args=['false']))
            except ValueError:
                context.update({
                    'task': task,
                    Constants.ERROR_FORM: {Constants.ERROR_SET: f'{Constants.VALUE_ERROR} Error deleting task'},
                })
                raise Constants.VALUE_ERROR
        else:
            context.update({Constants.ERROR_FORM: form.errors.items()})
            return render(request, 'task.html', context)
