from django.db import models


# Create your models here.

class Admin(models.Model):
    username=models.CharField(max_length=10,unique=True, verbose_name="username")
    password = models.CharField(max_length=10, unique=True, verbose_name="password")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    def __str__(self):
        return self.username