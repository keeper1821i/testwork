from django.urls import path
from rest_framework.routers import DefaultRouter

from .models import User
from .views import UserViewSet, UserListView

router = DefaultRouter()
router.register(r'clients/create', UserViewSet)
urlpatterns = [
    path('list', UserListView.as_view(), name='list'),
]

urlpatterns += router.urls
