from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=225)
    personal_number = models.CharField(max_length=11, unique=True, null=True)
    birth_date = models.DateField(null=True)

    def __str__(self):
        return self.email
