from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    gender = models.CharField(max_length=10, verbose_name='Пол')
    photo = models.ImageField(upload_to='photo/', default='photo/no_photo.jpg')

