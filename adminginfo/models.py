from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Create your models here.



#Gestionnaire de Models
class AdminManager(BaseUserManager):
    def create_user(self,username,password=None):
        if not username:
            raise ValueError("Le nom d'utilisateur est requis")


        if not password:
            raise ValueError("Le mot de passe est requis")

        user=self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user
class Admin(models.Model):
    username=models.CharField(max_length=10,unique=True, verbose_name="username")
    password = models.CharField(max_length=10, unique=True, verbose_name="password")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    objects = AdminManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password"]

    def __str__(self):
        return self.username