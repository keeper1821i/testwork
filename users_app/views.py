from rest_framework import status
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.core.mail import send_mail

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


def send_mail_to_like(sending_user, host_user):
    message = f"Вы понравились {sending_user.first_name}! Почта участника: {sending_user.email}"
    print(message)
    send_mail('Рассылка с сайта знакомств',
              message,
              sending_user.email,
              [host_user.email])


class PutALike(APIView):
    def put(self, request, pk):
        if request.user.id != pk:
            queryset = User.objects.get(id=pk)
            user_self = User.objects.get(id=request.user.id)
            likes = queryset.likes
            print(likes)
            if request.user.id in likes:
                send_mail_to_like(user_self, queryset)
                return Response('text', status.HTTP_200_OK)
            else:
                # user_self = User.objects.get(id=request.user.id)
                user_likes = user_self.likes
                user_likes.append(pk)
                user_self.likes = user_likes
                print(user_likes)
                user_self.save()
                return Response(likes)
        else:
            return Response('text', status.HTTP_200_OK)
