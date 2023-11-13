from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from datetime import timedelta

import requests
import json
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import Token, AccessToken, RefreshToken
from InstalledApps.general.constants import Constants
from InstalledApps.general import utils

from InstalledApps.general.exception_handlers import ExceptionHandler


def signup(request):
    context = {
        Constants.FORM: UserCreationForm,
        Constants.FORM_ACTION: '/signup/',
    }
    messages = []
    try:
        if request.method == 'POST':
            if request.POST['password1'] == request.POST['password2']:
                form = UserCreationForm(request.POST)
                if form.is_valid():
                    user = User.objects.create_user(
                        username=request.POST['username'],
                        password=request.POST['password1']
                    )
                    user.save()
                    login(request, user)  # create a cookie with user info
                    return redirect(reverse('index'))
                else:
                    context.update({
                        Constants.ERROR_FORM: form.errors.items()
                    })
                    raise ValidationError(str(form.errors.items()))
            else:
                messages.append('Password do not match')
                context.update({
                    Constants.ERROR_FORM: {Constants.ERROR_SET: messages}
                })
                raise ValueError(messages)
    except (ValidationError, ValueError) as e:
        ExceptionHandler(e).handle()
    except Exception as e:
        context.update({
            Constants.ERROR_FORM: {
                Constants.ERROR_SET: f'{Constants.ERROR_EXCEPTION} {e}'}
        })
        ExceptionHandler(e).handle()
    else:
        print(Constants.FORM_ELSE)
    finally:
        return render(request, 'signup.html', context)


@login_required
def signout(request):
    logout(request)
    return render(request, 'home.html', {
        Constants.FORM_TITLE: 'Home',
        Constants.FORM_CARD_TITLE: 'Home',
    })


def signin(request):
    context = {
        Constants.FORM: AuthenticationForm,
        Constants.FORM_ACTION: '/signin/'
    }
    if request.method == 'GET':
        return render(request, 'signin.html', context)
    elif request.method == 'POST':
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            context.update({Constants.ERROR_FORM: {
                           Constants.ERROR_SET: 'Username or password is incorrect'}})
            return render(request, 'signin.html', context)
        else:
            login(request, user)
            refresh = refresh_token(user, is_local=True)
            request.session[Constants.ACCESS_TOKEN] = str(refresh.access_token)
            request.session[Constants.REFRESH_TOKEN] = str(refresh)
            return redirect(reverse('index'))


# tokens manager, external calls in development
def access_token(user, is_local):
    token = None
    if is_local:
        # using token de django
        token = AccessToken.for_user(user)
        # __DEVELOPMENT__
        # token.set_exp(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
    # __DEVELOPMENT__
    else:
        data = {
            'username': user.username,
            'password': user.password,
        }

        headers = {
            Constants.FORM_CONTENT_TYPE: Constants.APLICATION_JSON
        }

        url_rest = f'{settings.API_BASE_URL}/api/token/'
        response = requests.post(url_rest, json=data, headers=headers)
        print(f"{url_rest} {token} {user.username} {user.password}")
        if response.status_code == 200:
            token = response.json().get('access')
            return token
        else:
            print(f'Error: {response.status_code} - {response.text}')
        return None
    return token


def refresh_token(user, is_local):
    token = None
    if is_local:
        # using token de django
        token = RefreshToken.for_user(user)
        # __DEVELOPMENT__
        # token.set_exp(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])
    # __DEVELOPMENT__ else:
    return token
