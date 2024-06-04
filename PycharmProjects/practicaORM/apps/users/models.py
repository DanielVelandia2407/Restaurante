from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    REQUIRED_FIELDS = ['email']

    #email = models.EmailField(unique=True)

    def save(self, *args, **kwargs) -> None:
        self.username = self.email.split('@')[0]
        return super().save(*args, **kwargs)
