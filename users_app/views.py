import django_filters
from django.db.models import F, DecimalField, ExpressionWrapper

from rest_framework import status
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.core.mail import send_mail
from .services import distance_on_sphere
from .serializers import UserRegisterSerializer, UserSerializer
from .models import User


class UserViewSet(ModelViewSet):
    """Апи для регистрации"""
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()


class UserFilter(filters.FilterSet):
    """Переопределенный FilterSet, для фильтрации по расстоянию"""
    class Meta:
        model = User
        distance = filters.FilterSet.form
        fields = ('first_name', 'last_name', 'gender', 'distance')

    distance = django_filters.NumberFilter(field_name='Расстояное', method='filter_distance')

    def filter_distance(self, queryset, name, value):
        queryset = queryset.filter(distance__lte=value)
        return queryset


class UserListView(ListAPIView):
    """Апи для вывода всех пользователей с возможностью фильтрации"""
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter

    def get_queryset(self):
        """Переопределенный Queryset, с добавленной дистанцией между пользователями"""
        queryset = User.objects.all()
        user = User.objects.get(id=self.request.user.id)
        user_coordinates = (user.latitude, user.longitude)
        queryset = queryset.annotate(distance=ExpressionWrapper(distance_on_sphere(F('latitude'),
                                                                                   F('longitude'),
                                                                                   user_coordinates[0],
                                                                                   user_coordinates[1]),
                                                                output_field=DecimalField()))
        return queryset


def send_mail_to_like(sending_user, host_user):
    """Стандартная функция отправки электронной почты"""
    message = f"Вы понравились {sending_user.first_name}! Почта участника: {sending_user.email}"
    print(message)
    send_mail('Рассылка с сайта знакомств',
              message,
              sending_user.email,
              [host_user.email])


class PutALike(APIView):
    """Апи оценки пользователя"""
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
