from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    personal_number = models.CharField(max_length=11, unique=True)
    birth_date = models.DateField(null=True)

    def __str__(self):
        return self.email
