from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/avatar/', null=True, blank=True)
    phone_number = models.CharField(max_length=100)

    def __str__(self):
        return self.username