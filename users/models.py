from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    personal_number = models.CharField(max_length=11, unique=True)
    birth_date = models.DateField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'personal_number', 'birth_date']

    def __str__(self):
        return self.email
