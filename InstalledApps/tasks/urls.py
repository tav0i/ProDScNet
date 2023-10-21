from django.urls import path
from InstalledApps.tasks import views

urlpatterns = [
    path('tasks/<str:is_not_completed>', views.tasks, name='tasks'),
    path('task/create/', views.task_create, name='task_create'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/complete', views.task_complete, name='task_complete'),
    path('task/<int:task_id>/delete', views.task_delete, name='task_delete'),
]