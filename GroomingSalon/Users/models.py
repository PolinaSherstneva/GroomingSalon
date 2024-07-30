from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone_number = models.CharField(max_length=100, verbose_name="Номер телефона", unique=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.phone_number

