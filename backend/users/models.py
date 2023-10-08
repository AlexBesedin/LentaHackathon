from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models


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
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.ADMIN,
    )
    
    def __str__(self):
        return f'{self.username}'

    @property
    def is_admin(self):
        return (self.role == Roles.ADMIN
                or self.is_superuser
                or self.is_staff)