from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer
from rest_framework import viewsets, permissions
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

@authentication_classes([JWTAuthentication])  
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TaskSerializer