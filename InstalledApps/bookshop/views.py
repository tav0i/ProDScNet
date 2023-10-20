from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Book
from .forms import BookForm

# Create your views here.
def bookshop_index(request):
    return render(request, 'pages/index.html')

@login_required
def bookshop(request):
    books = Book.objects.all()
    return render(request, 'bookshop.html', {
        'books':books
    })

@login_required
def bookshop_create(request):
    if request.method == 'GET':
        return render(request, 'bookshop_create.html', {
            'form': BookForm
        })
    elif request.method == 'POST':
        try:
            form = BookForm(request.POST)
            book = form.save(commit=False)
            book.save()
            return redirect('bookshop')
        except ValueError:
            return render(request, 'bookshop_create.html', {
                'form': BookForm,
                'error': 'Invalid data'
            })

@login_required
def bookshop_detail(request, book_id):
    return render(request, 'bookshop_detail.html')

@login_required  
def bookshop_delete(request, book_id):
    return redirect('bookshop')