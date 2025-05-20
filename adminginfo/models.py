from django.contrib.auth.hashers import make_password,check_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Create your models here.
class Admin(models.Model):
    username=models.CharField(max_length=10,unique=True, verbose_name="username")
    password = models.CharField(max_length=10, unique=True, verbose_name="password")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    def set_password(self, raw_password):
        """Hache le mot de passe brut et le stocke."""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Vérifie si le mot de passe brut correspond au hachage stocké."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username


class Annonce(models.Model):
    title=models.CharField(max_length=20,verbose_name="titre")
    corps=models.TextField(max_length=5000,verbose_name="Corps de l'annonce")
    piece=models.CharField(max_length=200)
    type_piece=models.CharField(max_length=100)
    date_ajout=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

