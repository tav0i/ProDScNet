from django.urls import path
from InstalledApps.bookshop import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', views.index, name='bookshop_index'),
    path('bookshop/', views.bookshop, name='bookshop'),
    path('bookshop_create/', views.bookshop_create, name='bookshop_create'),
    path('bookshop/<int:book_id>/', views.bookshop_detail, name='bookshop_detail'),
    path('bookshop/<int:book_id>/delete', views.bookshop_delete, name='bookshop_delete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)