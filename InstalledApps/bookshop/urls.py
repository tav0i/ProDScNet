from django.urls import path
from InstalledApps.bookshop import views

urlpatterns = [
    path('bookshop/', views.inicio, name='inicio'),
    path('pages/about_us/', views.about_us, name='about_us'),
]