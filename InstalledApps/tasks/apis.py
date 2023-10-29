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

@authentication_classes([JWTAuthentication])  
class TaskList(generics.ListCreateAPIView):
    authentication_classes = (JWTAuthentication,)
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        # Obtener el usuario autenticado
        user = request.user

        #Obtener las variables del query
        is_not_completed = self.kwargs.get('is_not_completed')
        if is_not_completed == 'False':
            is_not_completed = False
        else:
            is_not_completed = True

        queryset = Task.objects.filter(
            Q(user=self.request.user) &
            Q(date_completed__isnull=is_not_completed)).order_by('date_completed')
        
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

@authentication_classes([JWTAuthentication])  
class TaskCreate(generics.CreateAPIView):
    authentication_classes = (JWTAuthentication,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

@authentication_classes([JWTAuthentication])  
class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (JWTAuthentication,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer