from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'clients/create', UserViewSet)

urlpatterns = router.urls

