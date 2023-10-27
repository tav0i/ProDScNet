from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.conf import settings
from .models import Book
from .forms import BookForm

# Create your views here.


@login_required
def bookshop(request):
    books = Book.objects.all()
    return render(request, 'bookshop.html', {
        'books': books
    })


@login_required
def bookshop_create(request):
    context = {
        'form': BookForm,
        'formaction': '/bookshop/create/',
        'formenctype': 'multipart/form-data',
        'MEDIA_URL': settings.MEDIA_URL,
        'title': 'Create book',
        'cardtitle': 'Create book',
        'cardsubtitle': 'Book',
    }
    if request.method == 'GET':
        return render(request, 'bookshop_detail.html', context)
    elif request.method == 'POST':
        form = BookForm(request.POST, request.FILES or None)
        if form.is_valid():
            try:
                form.save()
                return redirect('bookshop')
            except ValueError:
                context.update({'errorform': {'errorset': 'Invalid data'}})
                return render(request, 'bookshop_detail.html', context)
        else:
            context.update({'errorform': form.errors.items()})
            return render(request, 'bookshop_detail.html', context)


@login_required
def bookshop_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    context = {
        'form': form,
        'formaction': f"/bookshop/'{book_id}/",
        'formenctype': 'multipart/form-data',
        'MEDIA_URL': settings.MEDIA_URL,
        'title': 'Edit book',
        'cardtitle': 'Edit book',
        'cardsubtitle': 'Book',
    }
    if request.method == 'GET':
        form = BookForm(instance=book)
        context.update({'book': book,}) 
        return render(request, 'bookshop_detail.html', context)
    elif request.method == 'POST':
        form = BookForm(request.POST, request.FILES or None, instance=book)
        if form.is_valid():
            try:
                form.save()
                return redirect('bookshop')
            except ValueError:
                context.update({
                    'book': book,
                    'errorform': {'errorset': 'Error updating book'}})
                return render(request, 'bookshop_detail.html', context)
        else:
            context.update({'errorform': form.errors.items()})
            return render(request, 'bookshop_detail.html', context)


@login_required
def bookshop_delete(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=book_id)
        try:
            book.delete()
            return redirect('bookshop')
        except ValueError:
            return render(request, 'bookshop.html', {
                'errorform': {'errorset': 'Error deleting book'}
            })
