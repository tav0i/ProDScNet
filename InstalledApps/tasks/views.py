from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required 
from django.db import IntegrityError
from django.utils import timezone
from .forms import TaskForm
from .forms import Task

# Create your views here.
def home(request):
    title = 'Hola mundo '
    return render(request, 'home.html')
                  
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                    )
                user.save()
                login(request, user) #create a cookie with user info
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Username already exists'
                })
        else:
            return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Password do not match'
                })

@login_required
def signout(request):
    logout(request)        
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    elif request.method == 'POST':
        user = authenticate(request, 
                     username= request.POST['username'],
                     password= request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'tasks.html',{
        'tasks': tasks,
        'title': 'Pending tasks'
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=False).order_by('date_completed')
    return render(request, 'tasks.html',{
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
        try:
            form = TaskForm(request.POST)
            user_task = form.save(commit=False)
            user_task.user = request.user
            user_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_create.html', {
            'form': TaskForm,
            'error': 'Invalid data'
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
        try:
            task = get_object_or_404(Task, pk=task_id, user = request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
            'task': task,
            'form': form,
            'error': "Error updating task"
        })

@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        return redirect('tasks')

@login_required  
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')