from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модоль пользователей"""
    gender = models.CharField(max_length=10, verbose_name='Пол')
    photo = models.ImageField(upload_to='photo/', default='photo/no_photo.jpg')
    likes = models.JSONField(blank=True, default=list)
    longitude = models.DecimalField(default=-58.573, decimal_places=3, max_digits=6)
    latitude = models.DecimalField(default=44.476, decimal_places=3, max_digits=6)

