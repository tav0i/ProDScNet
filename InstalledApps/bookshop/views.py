from django.shortcuts import render, redirect, get_object_or_404
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
        'books': books
    })


@login_required
def bookshop_create(request):
    if request.method == 'GET':
        return render(request, 'bookshop_create.html', {
            'form': BookForm,
            'formaction': '/bookshop/create/',
            'formenctype': 'multipart/form-data',
        })
    elif request.method == 'POST':
        form = BookForm(request.POST, request.FILES or None)
        if form.is_valid():
            try:
                form.save()
                return redirect('bookshop')
            except ValueError:
                return render(request, 'bookshop_create.html', {
                    'form': BookForm,
                    'formaction': '/bookshop/create/',
                    'formenctype': 'multipart/form-data',
                    'errorform': 'Invalid data'
                })
        else:
            errorform = "<ul>"
            for field, errors in form.errors.items():
                for error in errors:
                    errorform += f"<li>Error in '{field}': {error}</li>"
            errorform += "</ul>"
            return render(request, 'bookshop_create.html', {
                'form': BookForm,
                'formaction': '/bookshop/create/',
                'formenctype': 'multipart/form-data',
                "errorform": errorform
            })


@login_required
def bookshop_detail(request, book_id):
    if request.method == 'GET':
        book = get_object_or_404(Book, pk=book_id)
        form = BookForm(instance=book)
        return render(request, 'bookshop_detail.html', {
            'book': book,
            'form': form,
            'formaction': f"/bookshop/{book_id}/",
            'formenctype': 'multipart/form-data',
        })
    elif request.method == 'POST':
        book = get_object_or_404(Book, pk=book_id)
        form = BookForm(request.POST, request.FILES or None, instance=book)
        if form.is_valid():
            try:
                form.save()
                return redirect('bookshop')
            except ValueError:
                return render(request, 'bookshop_detail.html', {
                    'book': book,
                    'form': form,
                    'formaction': f"/bookshop/{book_id}/",
                    'formenctype': 'multipart/form-data',
                    'errorform': "Error updating book"
                })
        else:
            errorform = "<ul>"
            for field, errors in form.errors.items():
                for error in errors:
                    errorform += f"<li>Error in '{field}': {error}</li>"
            errorform += "</ul>"
            return render(request, 'bookshop_detail.html', {
                'form': form,
                'formaction': f"/bookshop/'{book_id}/",
                'formenctype': 'multipart/form-data',
                'errorform': errorform
            })


@login_required
def bookshop_delete(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=book_id)
        try:
            book.delete()
            return redirect('bookshop')
        except ValueError:
            return render(request, 'bookshop.html', {
                'errorform': "Error deleting book"
            })
