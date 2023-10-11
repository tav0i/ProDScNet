from django.shortcuts import render, redirect, get_object_or_404

def index(request):
    title = 'Hola mundo '
    return render(request, 'index.html')

def about_us(request):
    return render(request, 'about_us.html')
