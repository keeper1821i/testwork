from django.urls import path
from rest_framework.routers import DefaultRouter

from .models import User
from .views import UserViewSet, UserListView, PutALike

router = DefaultRouter()
router.register(r'clients/create', UserViewSet)
urlpatterns = [
    path('list', UserListView.as_view(), name='list'),
    path('clients/<int:pk>/match/', PutALike.as_view(), name='match')
]

urlpatterns += router.urls
