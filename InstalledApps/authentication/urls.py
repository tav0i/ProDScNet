from django.urls import path
from InstalledApps.authentication import views
from .apis import LoginView, RegisterView

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='login'),
]

urlpatterns += [
    path("api/login/", LoginView.as_view(), name="rest_login"),
    path("api/register/", RegisterView.as_view(), name="rest_register"),
]