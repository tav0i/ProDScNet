from django.shortcuts import render
from django.conf import settings
from InstalledApps.general.constants import Constants

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

def home(request):
    gretting = 'Saludos desde el programa de django'
    user = request.user
    context = {
        'gretting': gretting,
        'STATIC_URL_': settings.STATIC_URL,
        'MEDIA_ROOT_': settings.MEDIA_ROOT,
        'MEDIA_URL_': settings.MEDIA_URL,
        'BASE_DIR_': settings.BASE_DIR,
        'ACCESS_TOKEN_' : request.session.get(Constants.ACCESS_TOKEN),
        'REFRESH_TOKEN_': request.session.get(Constants.REFRESH_TOKEN),
    }
    return render(request, 'home.html', context)