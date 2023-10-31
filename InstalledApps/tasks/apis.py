from django.db.models import Q
from .models import Task
from .serializers import TaskSerializer
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenVerifyView

import requests
from .models import Task
from .serializers import TaskSerializer
from InstalledApps.general.constants import Constants


@authentication_classes([JWTAuthentication])
class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        user = request.user

        # Get the query variables
        is_not_completed = self.kwargs.get('is_not_completed')
        if is_not_completed == 'False':
            is_not_completed = False
        else:
            is_not_completed = True

        # Task.objects.select_related: ForeignKey o OneToOneField
        # Task.objects.prefetch_related ManyToManyField o Reverse ForeignKey
        # or in this case put UserSerializer inside TaskSerializer on serializer.py
        tasks_queryset = Task.objects.filter(
            Q(user=self.request.user) &
            Q(date_completed__isnull=is_not_completed)
        ).order_by('date_completed')
        tasks_serializer = self.serializer_class(tasks_queryset, many=True)

        return Response(tasks_serializer.data)


@authentication_classes([JWTAuthentication])
class TaskCreate(generics.CreateAPIView):
    authentication_classes = (JWTAuthentication,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


@authentication_classes([JWTAuthentication])
class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        task_id = self.kwargs.get('task_id')
        task_queryset = Task.objects.filter(
            Q(user=self.request.user) &
            Q(id=task_id)
        )

        # Verify if exist an element in queryset before to serialize
        if task_queryset.exists():
            task = task_queryset.first()
            task_serializer = self.serializer_class(task)  
            return Response(task_serializer.data)
        else:
            return Response({Constants.API_ERROR: "Task not found"}, status=404)

