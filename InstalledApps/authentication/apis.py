from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from InstalledApps.general.constants import Constants

class LoginView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                tokens = {
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                }
                response = Response()
                response.status_code = status.HTTP_200_OK
                response.data = tokens
                return response
            else:
                raise AuthenticationFailed(Constants.ERROR_INVALID_CREDENTIALS)
        except AuthenticationFailed as e:   
            return Response({
                Constants.ERROR_API: str(e)},
                status=status.HTTP_401_UNAUTHORIZED
                )
        except AssertionError as e:
            return Response({
                Constants.ERROR_API: str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
                )

# __DEVELOPMENT__ return token 
class RegisterView(APIView):
    def post(self, request):
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']

        user = User.objects.create_user(username, email, password)
        user.save()

        reponse = Response()
        response.status_code = status.HTTP_201_CREATED
        response.data = {Constants.MESSAGE_API: Constants.USER_REGISTERED}
        return response