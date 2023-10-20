from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required 
from django.db import IntegrityError

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    elif request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            form = UserCreationForm(request.POST)
            if form.is_valid():
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
                        "errorform": 'Username already exists'
                    })
                except ValueError:
                    return render(request, 'signup.html', {
                        'form': UserCreationForm,
                        'errorform': 'Invalid data'
                    })
            else:
                errorform = "<ul>"
                for field, errors in form.errors.items():
                    for error in errors:
                        errorform += f"<li>Error in '{field}': {error}</li>"
                errorform += "</ul>"
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "errorform": errorform
                })
        else:
            return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "errorform": 'Password do not match'
                })

@login_required
def signout(request):
    logout(request)        
    return render(request, 'home.html', {
        'title': 'Home',
        'cardtitle': 'Home',
    })

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
                'errorform': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')

