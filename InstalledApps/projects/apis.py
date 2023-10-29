from .models import Project
from .serializers import ProjectSerializer
from rest_framework import viewsets, permissions
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

@authentication_classes([JWTAuthentication])  
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProjectSerializer
