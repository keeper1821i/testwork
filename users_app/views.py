from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from rest_framework.viewsets import ModelViewSet

from .serializers import UserRegisterSerializer, UserSerializer
from .models import User


class UserViewSet(ModelViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()


class UserListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['first_name', 'last_name', 'gender']

