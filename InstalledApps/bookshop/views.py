from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.conf import settings
from django.urls import reverse
from .models import Book
from .forms import BookForm
from InstalledApps.general.constants import Constants
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
        Constants.FORM: BookForm,
        Constants.FORM_ACTION: '/bookshop/create/',
        Constants.FORM_ENCTYPE: 'multipart/form-data',
        Constants.MEDIA_URL: settings.MEDIA_URL,
        Constants.FORM_TITLE: 'Create book',
        Constants.FORM_CARD_TITLE: 'Create book',
        Constants.FORM_CARD_SUBTITLE: 'Book',
    }
    if request.method == 'GET':
        return render(request, 'bookshop_detail.html', context)
    elif request.method == 'POST':
        form = BookForm(request.POST, request.FILES or None)
        if form.is_valid():
            try:
                form.save()
                return redirect(reverse('bookshop'))
            except ValueError:
                context.update({
                    Constants.ERROR_FORM: {Constants.ERROR_SET: f'{Constants.INTEGRITY_ERROR} Invalid data'}
                    })
                raise {Constants.INTEGRITY_ERROR}
        else:
            context.update({Constants.ERROR_FORM: form.errors.items()})
            return render(request, 'bookshop_detail.html', context)


@login_required
def bookshop_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    context = {
        Constants.FORM_ACTION: f"/bookshop/{book_id}/",
        Constants.FORM_ENCTYPE: 'multipart/form-data',
        Constants.MEDIA_URL: settings.MEDIA_URL,
        Constants.FORM_TITLE: 'Edit book',
        Constants.FORM_CARD_TITLE: 'Edit book',
        Constants.FORM_CARD_SUBTITLE: 'Book',
    }
    if request.method == 'GET':
        form = BookForm(instance=book)
        context.update({
            Constants.FORM: form,
            'book': book,
            }) 
        return render(request, 'bookshop_detail.html', context)
    elif request.method == 'POST':
        form = BookForm(request.POST, request.FILES or None, instance=book)
        context.update({Constants.FORM: form})
        if form.is_valid():
            try:
                form.save()
                return redirect(reverse('bookshop'))
            except ValueError:
                context.update({
                    'book': book,
                    Constants.ERROR_FORM: {
                        Constants.ERROR_SET: f'{Constants.VALUE_ERROR} Error updating book'}
                        })
                raise {Constants.VALUE_ERROR}
        else:
            context.update({Constants.ERROR_FORM: form.errors.items()})
            return render(request, 'bookshop_detail.html', context)


@login_required
def bookshop_delete(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=book_id)
        try:
            book.delete()
            return redirect(reverse('bookshop'))
        except ValueError:
            context = {
                Constants.ERROR_FORM: {Constants.ERROR_SET: f'{Constants.VALUE_ERROR} Error deleting book'}
                }
            raise Constants.VALUE_ERROR
            return render(request, 'bookshop.html', {
                Constants.ERROR_FORM: {Constants.ERROR_SET: 'Error deleting book'}
            })
