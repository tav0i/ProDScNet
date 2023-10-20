from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 

@login_required
def index(request):
    content = 'Welcome to index page'
    return render(request, 'index.html', {
        'content': content,
    })

def about_us(request):
    return render(request, 'about_us.html')
