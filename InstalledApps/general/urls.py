from django.urls import path
from InstalledApps.general import views

urlpatterns = [
    path('general/index', views.index, name='index'),
    path('general/about_us', views.about_us, name='about_us'),
]