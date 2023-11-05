"""
URL configuration for ProDScNet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from InstalledApps.general.views import Error404View, Error500View
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.png')),
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Others paths protected by JWT
    # path('api/secure-resource/', views.SecureResourceView.as_view(), name='secure_resource'),

    path('', include('InstalledApps.authentication.urls')),
    path('', include('InstalledApps.general.urls')),
    path('', include('InstalledApps.tasks.urls')),
    path('', include('InstalledApps.bookshop.urls')),
    path('', include('InstalledApps.projects.urls')),
]

handler404 = Error404View.as_view()

handler500 = Error500View.as_error_view()
