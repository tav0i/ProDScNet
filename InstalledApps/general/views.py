from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponseServerError
from django.views.generic import (
    TemplateView,
    View,
    ListView,
    DetailView
)



@login_required
def index(request):
    content = 'Welcome to index page'
    return render(request, 'pages/index.html', {
        'content': content,
    })

def about_us(request):
    return render(request, 'about_us.html')


class Error404View(TemplateView):
    template_name = 'error404.html'


class Error500View(TemplateView):
    template_name = 'error500.html'

    @classmethod
    def as_error_view(cls):
        def view(request):
            v = cls.as_view()
            r = v(request)
            r.render()
            return r
        return view