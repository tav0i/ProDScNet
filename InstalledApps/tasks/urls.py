from django.urls import path
from InstalledApps.tasks import views

urlpatterns = [
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete', views.task_complete, name='task_complete'),
    path('tasks/<int:task_id>/delete', views.task_delete, name='task_delete'),
    path('tasks/create/', views.task_create, name='task_create'),
]