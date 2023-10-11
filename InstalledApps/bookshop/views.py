from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required 
from .models import Book

# Create your views here.
def index(request):
    return render(request, 'pages/index.html')

def bookshop(request):
    books = Book.objects.all()
    return render(request, 'bookshop.html', {
        'books':books
    })

def bookshop_create(request):
    return render(request, 'bookshop_create.html')

def bookshop_detail(request, book_id):
    return render(request, 'bookshop_detail.html')

@login_required  
def bookshop_delete(request, book_id):
    return redirect('bookshop')