from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


def signup(request):
    context = {
        'form': UserCreationForm,
        'formaction': '/signup/',
    }
    if request.method == 'GET':
        return render(request, 'signup.html', context)
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
                    login(request, user)  # create a cookie with user info
                    return redirect(reverse('index'))
                except IntegrityError:
                    context.update(
                        {'errorform': {'errorset': 'Username already exists'}})
                    return render(request, 'signup.html', context)
                except ValueError:
                    context.update({'errorform': {'errorset': 'Invalid data'}})
                    return render(request, 'signup.html', context)
            else:
                context.update({'errorform': form.errors.items()})
                return render(request, 'signup.html', context)
        else:
            context.update({
                'formaction': '',
                'errorform': {'errorset': 'Password do not match'}
            })
            return render(request, 'signup.html', context)


@login_required
def signout(request):
    logout(request)
    return render(request, 'home.html', {
        'title': 'Home',
        'cardtitle': 'Home',
    })


def signin(request):
    context = {
        'form': AuthenticationForm,
        'formaction': '/signin/'
    }
    if request.method == 'GET':
        return render(request, 'signin.html', context)
    elif request.method == 'POST':
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            context.update({'errorform': {'errorset': 'Username or password is incorrect'}})
            return render(request, 'signin.html', context)
        else:
            login(request, user)
            return redirect(reverse('index'))
