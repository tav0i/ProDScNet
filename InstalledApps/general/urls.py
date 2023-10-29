from django.urls import path
from django.views.generic import TemplateView
from InstalledApps.general import views

urlpatterns = [
    path('pages/', TemplateView.as_view(template_name='pages/index.html'), name='index'),
    path('general/about_us/', views.about_us, name='about_us'),
]