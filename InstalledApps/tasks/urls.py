from django.urls import path
from InstalledApps.tasks import views
from InstalledApps.tasks import apis
from .apis import TaskViewSet

from rest_framework import routers

urlpatterns = [
    # path('api/tasks/<str:is_not_completed>/', apis.TaskList.as_view(), name='api_tasks'),
    # path('api/task/<int:task_id>/', apis.TaskDetail.as_view(), name='api_task_detail'),
    # path('api/task/create/', apis.TaskCreate.as_view(), name='api_task_create'),

    path('tasks/<str:is_not_completed>/', views.tasks, name='tasks'),
    path('task/create/', views.task_create, name='task_create'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/complete', views.task_complete, name='task_complete'),
    path('task/<int:task_id>/delete', views.task_delete, name='task_delete'),
]

router = routers.DefaultRouter()
router.register('api/tasks', TaskViewSet, 'tasks')
urlpatterns += router.urls