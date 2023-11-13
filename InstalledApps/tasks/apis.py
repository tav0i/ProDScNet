from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User, Group
#from django.contrib.auth.decorators import permission_required
from .models import Task
from .serializers import TaskSerializer
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied, ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from InstalledApps.general.constants import Constants

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TaskSerializer

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class TaskViewList(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    allowed_methods = ['GET',]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            group = Group.objects.filter(user=user, name=Constants.ALLOW_VIEWER)
            if not group.exists():
                raise PermissionDenied(Constants.ERROR_PERMISION_DENIED)
            # Get the query variables
            is_not_completed = self.kwargs.get('is_not_completed').lower()
            if is_not_completed == 'false':
                is_not_completed = False
            elif is_not_completed == 'true':
                is_not_completed = True
            else:
                raise ValidationError(Constants.ERROR_VALIDATION)

            # __IMPORTANT__
            # Task.objects.select_related: ForeignKey o OneToOneField
            # Task.objects.prefetch_related ManyToManyField o Reverse ForeignKey
            # or in this case put UserSerializer inside TaskSerializer on serializer.py
            tasks_queryset = Task.objects.filter(
                Q(user=self.request.user) &
                Q(date_completed__isnull=is_not_completed)
            ).order_by('date_completed')

            tasks_serializer = self.serializer_class(tasks_queryset, many=True)
            if tasks_queryset.exists():
                return Response(tasks_serializer.data, status=status.HTTP_200_OK)
            else:
                raise NotFound(Constants.ERROR_TASK_NOT_FOUND)
        except NotFound as e:
            return Response({
                Constants.ERROR_API: str(e)}, 
                status=status.HTTP_404_NOT_FOUND
                )
        except ValidationError as e:
            return Response({
                Constants.ERROR_API: str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
                )
        except PermissionDenied as e:
            return Response({
                Constants.ERROR_API: str(e)}, 
                status=status.HTTP_403_FORBIDDEN
                )

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class TaskViewDetail(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    allowed_methods = ['GET',]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            group = Group.objects.filter(user=user, name=Constants.ALLOW_VIEWER)
            if not group.exists():
                raise PermissionDenied(Constants.ERROR_PERMISION_DENIED)
            task_id = self.kwargs.get('task_id')
            task_queryset = Task.objects.filter(
                Q(user=self.request.user) &
                Q(id=task_id)
            )
            if task_queryset.exists():
                task = task_queryset.first()
                task_serializer = self.serializer_class(task)  
                return Response(task_serializer.data, status=status.HTTP_200_OK)
            else:
                raise NotFound(Constants.ERROR_TASK_NOT_FOUND)
        except NotFound as e:
            return Response({
                Constants.ERROR_API: str(e)}, 
                status=status.HTTP_404_NOT_FOUND
                )
        except PermissionDenied as e:
            return Response({
                Constants.ERROR_API: str(e)}, 
                status=status.HTTP_403_FORBIDDEN
                )

# __DEVELOPMENT__
@authentication_classes([JWTAuthentication])
class TaskCreate(generics.CreateAPIView):
    authentication_classes = (JWTAuthentication,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer