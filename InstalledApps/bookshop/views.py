from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def inicio(request):
    return HttpResponse("<h1>Bienvenido</h1>")

def about_us(request):
    return render(request, 'pages/about_us.html')