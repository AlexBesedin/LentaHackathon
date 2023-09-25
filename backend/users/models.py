from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractUser


class Roles(models.TextChoices):
    USER = 'user'
    ADMIN = 'admin'


class CustomUser(AbstractUser):
    """ Кастомная модель пользователя. """
    username = models.CharField(
        max_length=150,
        verbose_name = 'Логин', 
        unique=True,
        validators=[validators.RegexValidator(regex='^[\w.@+-]+$')]
        )
    email = models.EmailField(
        max_length=254, 
        verbose_name = 'Email',
        unique=True
        )
    first_name = models.CharField(
        max_length=150,
        verbose_name = 'Имя'
        )
    last_name = models.CharField(
        max_length=150,
        verbose_name = 'Фамилия'
        )
    date_joined = models.DateTimeField(
        auto_now_add=True
        )
    is_active = models.BooleanField(
        default=True
        )
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USER,
    )
    
    def __str__(self):
        return f'{self.username}'

    @property
    def is_admin(self):
        return (self.role == Roles.ADMIN
                or self.is_superuser
                or self.is_staff)