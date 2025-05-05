from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin


#Gestionnaire de Models
class EtudiantManager(BaseUserManager):
    def create_user(self,matricule,password=None):
        if not matricule:
            raise ValueError("Le matricule est requis")


        if not password:
            raise ValueError("Le mot de passe est requis")

        user=self.model(
            matricule=matricule,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,matricule,password=None):
        user=self.create_user(
            matricule=matricule,
            password=password,
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class Etudiant(AbstractBaseUser,PermissionsMixin):
    matricule=models.CharField(max_length=10,unique=True,verbose_name="identifiant")
    nom=models.CharField(max_length=255,verbose_name="nom")
    prenom=models.CharField(max_length=255,verbose_name="prenom")
    password = models.CharField(max_length=10,verbose_name="mot de passe")
    annee=models.CharField(max_length=4,verbose_name="annee d'inscription",default=0)
    niveau=models.CharField(max_length=9,default=0,verbose_name="niveau")
    filiere =models.CharField(max_length=4,verbose_name="filiere",default=0)
    profil=models.CharField(max_length=255,verbose_name="profil")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff= models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects=EtudiantManager()
    USERNAME_FIELD="matricule"
    REQUIRED_FIELDS = ["password"]

    def __str__(self):
        return self.matricule

