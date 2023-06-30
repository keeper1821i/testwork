from django.db.models import F, DecimalField, ExpressionWrapper
from rest_framework import status
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.core.mail import send_mail
from geopy.distance import geodesic as GC

from .serializers import UserRegisterSerializer, UserSerializer
from .models import User


class UserViewSet(ModelViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()


class CustomFilter(filters.DjangoFilterBackend):

    def filter_queryset(self, request, queryset, view):
        user = User.objects.get(id=request.user.id)
        user_coordinates = (user.latitude, user.longitude)
        queryset = super().filter_queryset(request, queryset, view)
        queryset = queryset.annotate(distance=GC(user_coordinates, ('{k}{x}'.format(k=F('latitude'),
                                                                                    x=F('longitude')))))

        print(queryset.values('distance')[0])
        return queryset

class UserListView(ListAPIView):
    serializer_class = UserSerializer
    filter_backends = (CustomFilter,)
    distance = 0
    filterset_fields = ['first_name', 'last_name', 'gender']

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset



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
