from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from InstalledApps.general.constants import Constants

def home(request):
    gretting = 'Saludos desde el programa de django'
    context = {
        'gretting': gretting,
        'STATIC_URL_': settings.STATIC_URL,
        'MEDIA_ROOT_': settings.MEDIA_ROOT,
        'MEDIA_URL_': settings.MEDIA_URL,
        'BASE_DIR_': settings.BASE_DIR,
        'ACCESS_TOKEN_' : request.session.get(Constants.ACCESS_TOKEN)
    }
    return render(request, 'home.html', context)