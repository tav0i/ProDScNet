from rest_framework import routers
from .apis import ProjectViewSet

router = routers.DefaultRouter()
router.register('api/projects', ProjectViewSet, 'projects')

urlpatterns = router.urls