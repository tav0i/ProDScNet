from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from requests.exceptions import HTTPError
from .forms import Task, TaskForm
from .serializers import TaskSerializer #, TaskDecoder

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
    messages = []
    try:
        if is_not_completed == 'False':
            is_not_completed = False
            context.update({
                Constants.FORM_TITLE: 'Completed Task',
                Constants.FORM_ACTION: '/task/False'
            })
        elif is_not_completed == 'True':
            is_not_completed = True
            context.update({
                Constants.FORM_TITLE: 'Pending Task',
                Constants.FORM_ACTION: '/task/True'
            })
        else:
            messages.append('Option not available, default Pending task')
            is_not_completed = True
            context.update({
                Constants.FORM_TITLE: 'Pending Task',
                Constants.FORM_ACTION: '/task/True',
                Constants.ERROR_FORM: {Constants.ERROR_SET: messages}
            })
            raise Exception(messages)
        tasks = Task.objects.filter(
            user=request.user,
            date_completed__isnull=is_not_completed).order_by('date_completed')
        context.update({
            'tasks': tasks,
        })
        # call to REST
        rest_url = f'{settings.API_BASE_URL}api/tasks/{is_not_completed}/'
        access_token = str(request.session.get(Constants.ACCESS_TOKEN))
        headers = {
            Constants.AUTHORIZATION: f'{Constants.AUTORIZATION_TYPE} {access_token}'
        }
        data = {}
        response = requests.get(rest_url, headers=headers, data=data)
        print(f'Status code: " {response.status_code}')
        if response.status_code == 200:
            task_rest_data = response.json()
            # Crear una lista de instancias de Task
            task_instances = [Task(**data) for data in task_rest_data]
            # Pasar la lista de instancias al serializador
            tasks_serializer = TaskSerializer(
                instance=task_instances, many=True)
            print(f'EN TASK_SERIALIZER {tasks_serializer}')
            # Deserializar la respuesta a una lista de Task
            # print(response.json)
            # task_list = json.loads(response.content, cls=TaskDecoder)
            # print(f'REST json : {task_list}')
            # print(task.id)
            # print(task.title)
            # print(task.user.username)
            # print(task.user.email)

            # print(f'REST: {task_rest_data}')
            # print(f'SERIALIZADOS: {tasks_serializer}')
            if tasks_serializer.is_valid():
                print(f'Task serializer valido')
            else:
                print(f'Task serializer invalid')
                # raise HTTPError('task serializer invalid')
            #    print(f'messsages: {tasks_serializer.error_messages}')
            #   context.update({
            #       Constants.ERROR_FORM: tasks_serializer.error_messages
            #   })
        else:
            print(f'task serializer fail {response.status_code}')
            # raise HTTPError(f'task serializer invalid {response.status_code}')
    except HTTPError as e:
        context.update({
            Constants.ERROR_FORM: {
                Constants.ERROR_SET: f'{Constants.ERROR_HTTP_REST} {e}'}
        })
    except Exception as e:
        context.update({
            Constants.ERROR_FORM: {
                Constants.ERROR_SET: f'{Constants.ERROR_EXCEPTION} {e}'}
        })
    else:
        print('executed if no not exist error')
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
                return redirect(reverse('tasks', args=['True']))
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
        # __IMPORTANT__ call to de Models directly
        task = get_object_or_404(
            Task,
            pk=task_id,
            user=request.user
        )
        if request.method == 'GET':
            form = TaskForm(instance=task)
            context.update({
                Constants.FORM: form,
            })
            context.update({
                'task': task,
            })
            ###
            task_serializer = TaskSerializer(
                instance=task, many=False
            )
            print(f'SERIALIZADO DIRECTO:  {task_serializer.data}')
            ###

            rest_url = f'{settings.API_BASE_URL}api/task/{task_id}/'
            access_token = str(request.session.get(Constants.ACCESS_TOKEN))
            headers = {
                Constants.AUTHORIZATION: f'{Constants.AUTORIZATION_TYPE} {access_token}'
            }
            data = {}
            response = requests.get(rest_url, headers=headers, data=data)
            if response.status_code == 200:
                task_rest_data = response.json()
                print(f'TASK_REST_DATA_RESPONSE {task_rest_data}')

                # data_json = '{"id":1,"title":"tarea de deploy hacia google cloud","description":"tarea de deploy hacia google cloud desde git","is_important":true,"date_completed":null,"user": {"id":1,"username":"tav0i","email":"tav0i@outlook.com"}}'
                # print(f'DATA_JSON {data_json}')

                tasks_serializer = TaskSerializer(
                    data=task_rest_data, many=False
                )
                if tasks_serializer.is_valid():

                    # Convert the serialized data to JSON
                    renderer = JSONRenderer()
                    task_rest = renderer.render(tasks_serializer.data)
                    print(
                        f'EN TASK_REST_DATA {task_rest} - {tasks_serializer.is_valid()}'
                    )
                    # Decode the JSON data into a Task object
                    # task_object = json.loads(task_rest, cls=TaskDecoder)
                    # print("JSON_LOAD:", task_object)

                    context.update({
                        'task': task,
                    })
                    print(f"DESERIALIZATION SUCESS!!!")
                else:
                    print("Errors during deserialization:",
                          task_serializer.errors)
                    # raise HTTPError('task serializer invalid')
                #    print(f'messsages: {tasks_serializer.error_messages}')
                #   context.update({
                #       Constants.ERROR_FORM: tasks_serializer.error_messages
                #   })

                # context.update({
                #     'task': tasks_serializer,
                # })
                # print(f'EN TASK_SERIALIZER {tasks_serializer}')

            else:
                print(f'task serializer fail {response.status_code}')
                # raise HTTPError(f'task serializer invalid {response.status_code}')
    except HTTPError as e:
        context.update({
            Constants.ERROR_FORM: {
                Constants.ERROR_SET: f'{Constants.ERROR_HTTP_REST} {e}'}
        })
    except Exception as e:
        print(f'Exception {e}')
        context.update({
            Constants.ERROR_FORM: {
                Constants.ERROR_SET: f'{Constants.ERROR_EXCEPTION} {e}'}
        })
    else:
        print('se ejecuta si no hay excepcion')
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
                    return redirect(reverse('tasks', args=['True']))
                else:
                    return redirect(reverse('tasks', args=['False']))
            except ValueError:
                context.update({
                    'task': task,
                    Constants.ERROR_FORM: {Constants.ERROR_SET: f'{Constants.VALUE_ERROR} Error deleting task'},
                })
                raise Constants.VALUE_ERROR
        else:
            context.update({Constants.ERROR_FORM: form.errors.items()})
            return render(request, 'task.html', context)
